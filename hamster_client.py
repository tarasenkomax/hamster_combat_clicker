import logging
import re
from base64 import b64decode
from http import HTTPStatus
from time import sleep, time
from typing import Dict, Union

from requests import Response, Session

from config import HEADERS, MORSE_CODE_DICT
from enums import MessageEnum, UrlsEnum
from mixins import TimestampMixin, CardSorterMixin

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s   %(message)s")


def retry(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                result = func(*args, **kwargs)
                if result.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED):
                    return result
                else:
                    logging.info(MessageEnum.MSG_BAD_RESPONSE.format(status=result.status_code, text=result.text))
                    sleep(10)
            except Exception as error:
                logging.error(MessageEnum.MSG_SESSION_ERROR.format(error=error))
                sleep(1)

    return wrapper


class HamsterClient(Session, TimestampMixin, CardSorterMixin):
    state: Dict = None
    boosts: Dict = None
    upgrades: Dict = None
    task_checked_at: float = None

    def __init__(self, token, name="NoName", **kwargs) -> None:
        super().__init__()
        self.features = kwargs
        self.headers: Dict = HEADERS.copy()
        self.headers["Authorization"]: str = f"Bearer {token}"
        self.request = retry(super().request)
        self.name: str = name

    @property
    def balance(self) -> Union[int, None]:
        """ Количество заработанных монет """
        if self.state:
            return int(self.state["balanceCoins"])

    @property
    def level(self) -> Union[int, None]:
        """ Текущий уровень """
        if self.state:
            return self.state["level"]

    @property
    def available_taps(self) -> Union[int, None]:
        """ Энергия """
        if self.state:
            return self.state["availableTaps"]

    @property
    def recover_per_sec(self) -> Union[int, None]:
        """ Востановление энергии в секунду """
        if self.state:
            return self.state["tapsRecoverPerSec"]

    @property
    def is_taps_boost_available(self) -> Union[bool, None]:
        """ Проверка, доступны ли усиления """
        self.update_boosts_list()
        if not self.boosts:
            return
        for boost in self.boosts["boostsForBuy"]:
            if (
                boost["id"] == 'BoostFullAvailableTaps'
                and boost["cooldownSeconds"] == 0
                and boost["level"] <= boost["maxLevel"]
            ):
                return True

    @property
    def stats(self) -> Dict:
        """ Статистика """
        return {
            "уровень": self.level,
            "энергия": self.available_taps,
            'баланс': re.sub(r'(?<!^)(?=(\d{3})+$)', ' ', str(self.balance)),
            "доход в час": re.sub(r'(?<!^)(?=(\d{3})+$)', ' ', str(self.state['earnPassivePerHour']))
        }

    @property
    def log_prefix(self) -> str:
        """ Префикс с именем пользователя для логирования """
        return f"[{self.name}]\t "

    def get_cipher_data(self) -> Dict:
        """
        Получить информацио о шифре

        Example:
            {
                'cipher': 'REV4GSQ==',
                'bonusCoins': 1000000,
                'isClaimed': True,
                'remainSeconds': 27144
            }
        """
        result = self.post(url=UrlsEnum.CONFIG).json()
        return result['dailyCipher']

    def claim_daily_cipher(self) -> None:
        """ Разгадываем шифр """
        cipher_data = self.get_cipher_data()
        if not cipher_data['isClaimed']:
            raw_cipher = cipher_data['cipher']
            logging.info(MessageEnum.MSG_CRYPTED_CIPHER.format(cipher=raw_cipher))
            re_result = re.search('\d+', raw_cipher[3:])  # noqa W605
            if re_result:
                str_len = re_result[0]
                raw_cipher = raw_cipher.replace(str_len, "", 1)
                raw_cipher = raw_cipher.encode()
                cipher = b64decode(raw_cipher).decode()
                morse_cipher = "  ".join((MORSE_CODE_DICT.get(char, " ") for char in cipher))
                logging.info(MessageEnum.MSG_CIPHER.format(cipher=cipher + " | " + morse_cipher))
                self.post(url=UrlsEnum.CLAIM_DAILY_CIPHER, json={"cipher": cipher})

    def sync(self) -> None:
        """ Обновить данные о пользователе """
        try:
            response = self.post(url=UrlsEnum.SYNC)
            self.state = response.json()["clickerUser"]
            logging.info(self.log_prefix + MessageEnum.MSG_SYNC)
        except Exception as error:
            logging.error(self.log_prefix + MessageEnum.MSG_SYNC_ERROR.format(error=error))

    def check_task(self) -> None:
        """ Получение ежедневной награды """
        data = {
            "taskId": "streak_days"
        }
        if not self.task_checked_at or time() - self.task_checked_at >= 60 * 60:
            self.post(url=UrlsEnum.CHECK_TASK, json=data)
            self.task_checked_at = time()

    def tap(self) -> None:
        """ Тапаем на монеты максимальное кол-во раз """
        taps_count = self.available_taps or self.recover_per_sec
        data = {
            "count": taps_count,
            "availableTaps": self.available_taps - taps_count,
            "timestamp": self.timestamp()
        }
        self.post(url=UrlsEnum.TAP, json=data).json()
        logging.info(self.log_prefix + MessageEnum.MSG_TAP.format(taps_count=taps_count))

    def apply_boost(self, boost_name='BoostFullAvailableTaps') -> None:
        """
        Взять усиление
        :param boost_name: название усиления
        """
        data = {
            "boostId": boost_name,
            "timestamp": self.timestamp()
        }
        self.post(url=UrlsEnum.BUY_BOOST, json=data)

    def upgrade_card(self, upgrade_name) -> Response:
        """
        Купить карточку
        :param upgrade_name: название карточки
        """
        data = {
            "upgradeId": upgrade_name,
            "timestamp": self.timestamp()
        }
        response = self.post(url=UrlsEnum.BUY_UPGRADE, json=data)
        return response

    def upgrades_list(self) -> None:
        """ Обновить список карточек """
        self.upgrades = self.post(url=UrlsEnum.UPGRADES_FOR_BUY).json()

    def update_boosts_list(self) -> None:
        """
        Обновить список усилиений
         - BoostEarnPerTap
         - BoostMaxTaps
         - BoostFullAvailableTaps
         """
        self.boosts = self.post(url=UrlsEnum.BOOSTS_FOR_BUY).json()

    def get_sorted_upgrades(self, method):
        """
            1. Фильтруем карточки
                - доступные для покупки
                - не просроченные
                - с пассивным доходом
                - без ожидания перезарядки
            2. Сортируем по профитности на каждую потраченную монету
        """
        methods = dict(
            payback=self.sorted_by_payback,
            price=self.sorted_by_price,
            profit=self.sorted_by_profit,
            profitness=self.sorted_by_profitness
        )
        prepared = []
        for upgrade in self.upgrades.get("upgradesForBuy"):
            if (
                upgrade["isAvailable"]
                and not upgrade["isExpired"]
                and upgrade["profitPerHourDelta"] > 0
                and not upgrade.get("cooldownSeconds")
            ):
                item = upgrade.copy()
                if 'condition' in item:
                    item.pop('condition')
                prepared.append(item)
        if prepared:
            sorted_items = [i for i in methods[method](prepared)]
            return sorted_items
        return []

    def buy_upgrades(self) -> None:
        """ Покупаем лучшие апгрейды на все монеты """
        if self.features['buy_upgrades']:
            while True:
                self.upgrades_list()
                if sorted_upgrades := self.get_sorted_upgrades(self.features['buy_decision_method']):
                    upgrade = sorted_upgrades[0]
                    if upgrade['price'] <= self.balance:
                        result = self.upgrade_card(upgrade['id'])
                        if result.status_code == HTTPStatus.OK:
                            self.state = result.json()["clickerUser"]

                        log_info = {
                            'name': upgrade['name'],
                            'price': re.sub(r'(?<!^)(?=(\d{3})+$)', ' ', str(upgrade['price'])),
                            'level': upgrade['level'],
                            'profitPerHourDelta': re.sub(
                                r'(?<!^)(?=(\d{3})+$)',
                                ' ',
                                str(upgrade['profitPerHourDelta'])
                            ),
                        }

                        logging.info(self.log_prefix + MessageEnum.MSG_BUY_UPGRADE.format(**log_info))
                        sleep(0.5)
                    else:
                        break
                else:
                    break
        else:
            self.upgrades_list()

    def claim_combo_reward(self) -> None:
        """ Получаем награду, если собрано комбо """
        combo = self.upgrades.get('dailyCombo', {})
        upgrades = combo.get('upgradeIds', [])
        combo_cards = ", ".join(upgrades)
        logging.info(self.log_prefix + MessageEnum.MSG_CLAIMED_COMBO_CARDS.format(cards=combo_cards or '-'))
        if combo and len(upgrades) == 3:
            if combo.get('isClaimed') is False:
                result = self.post(url=UrlsEnum.CLAIM_DAILY_COMBO)
                if result.status_code == HTTPStatus.OK:
                    self.state = result.json()["clickerUser"]
                    logging.info(self.log_prefix + MessageEnum.MSG_COMBO_EARNED.format(coins=combo['bonusCoins']))
