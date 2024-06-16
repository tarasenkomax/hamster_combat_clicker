import logging
import re
from base64 import b64decode
from http import HTTPStatus
from time import sleep, time
from typing import Dict, Union

import aiohttp

from config import HEADERS, MORSE_CODE_DICT
from enums import MessageEnum, UrlsEnum
from mixins import CardSorterMixin, TimestampMixin

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s   %(message)s")


class HamsterClient(TimestampMixin, CardSorterMixin):
    state: Dict = None
    boosts: Dict = None
    upgrades: Dict = None
    task_checked_at: float = None

    def __init__(self, token, name="NoName", **kwargs) -> None:
        self.token: str = token
        self.features = kwargs
        self.name: str = name
        self._session = aiohttp.ClientSession(headers=self._headers)

    @property
    def _headers(self) -> Dict:
        headers: Dict = HEADERS.copy()
        headers["Authorization"]: str = f"Bearer {self.token}"
        return headers

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
    async def is_taps_boost_available(self) -> Union[bool, None]:
        """ Проверка, доступны ли усиления """
        await self.update_boosts_list()
        if not self.boosts:
            return False
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

    async def get_cipher_data(self) -> Dict:
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
        async with self._session.request(method="POST", url=UrlsEnum.CONFIG) as response:
            response.raise_for_status()
            response_data = await response.json()
            return response_data['dailyCipher']

    async def claim_daily_cipher(self) -> None:
        """ Разгадать шифр """
        cipher_data = await self.get_cipher_data()
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
                async with self._session.request(method="POST", url=UrlsEnum.CLAIM_DAILY_CIPHER) as response:
                    response.raise_for_status()

    async def sync(self) -> None:
        """ Обновить данные о пользователе """
        try:
            async with self._session.request(method="POST", url=UrlsEnum.SYNC) as response:
                response.raise_for_status()
                response_data = await response.json()
                self.state = response_data["clickerUser"]
                logging.info(self.log_prefix + MessageEnum.MSG_SYNC)
        except Exception as error:
            logging.error(self.log_prefix + MessageEnum.MSG_SYNC_ERROR.format(error=error))

    async def check_task(self) -> None:
        """ Получить ежедневную награду """
        data = {
            "taskId": "streak_days"
        }
        if not self.task_checked_at or time() - self.task_checked_at >= 60 * 60:
            async with self._session.request(method="POST", url=UrlsEnum.CHECK_TASK, json=data) as response:
                response.raise_for_status()
                self.task_checked_at = time()

    async def tap(self) -> None:
        """ Тапнуть на монеты максимальное кол-во раз """
        taps_count = self.available_taps or self.recover_per_sec
        data = {
            "count": taps_count,
            "availableTaps": self.available_taps - taps_count,
            "timestamp": self.timestamp()
        }

        async with self._session.request(method="POST", url=UrlsEnum.TAP, json=data) as response:
            response.raise_for_status()
            logging.info(self.log_prefix + MessageEnum.MSG_TAP.format(taps_count=taps_count))

    async def apply_boost(self, boost_name='BoostFullAvailableTaps') -> None:
        """
        Взять усиление
        :param boost_name: название усиления
        """
        data = {
            "boostId": boost_name,
            "timestamp": self.timestamp()
        }
        async with self._session.request(method="POST", url=UrlsEnum.BUY_BOOST, json=data) as response:
            response.raise_for_status()

    async def upgrade_card(self, upgrade_name) -> Dict:
        """
        Купить карточку
        :param upgrade_name: название карточки
        """
        data = {
            "upgradeId": upgrade_name,
            "timestamp": self.timestamp()
        }

        async with self._session.request(method="POST", url=UrlsEnum.BUY_UPGRADE, json=data) as response:
            response.raise_for_status()
            response_code = response.status
            response_data = await response.json()

            return dict(
                status_code=response_code,
                data=response_data
            )

    async def upgrades_list(self) -> None:
        """ Обновить список карточек """
        async with self._session.request(method="POST", url=UrlsEnum.UPGRADES_FOR_BUY) as response:
            response.raise_for_status()
            self.upgrades = await response.json()

    async def update_boosts_list(self) -> None:
        """
        Обновить список усилиений
         - BoostEarnPerTap
         - BoostMaxTaps
         - BoostFullAvailableTaps
         """
        async with self._session.request(method="POST", url=UrlsEnum.BOOSTS_FOR_BUY) as response:
            response.raise_for_status()
            self.boosts = await response.json()

    def get_sorted_upgrades(self, method):
        """
            1. Отфильтровать карточки
                - доступные для покупки
                - не просроченные
                - с пассивным доходом
                - без ожидания перезарядки
            2. Отсортировать в соответствии с выбранным методом
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

    async def buy_upgrades(self) -> None:
        """ Покупаем лучшие апгрейды на все монеты """
        if self.features['buy_upgrades']:
            while True:
                await self.upgrades_list()
                if sorted_upgrades := self.get_sorted_upgrades(self.features['buy_decision_method']):
                    upgrade = sorted_upgrades[0]
                    if upgrade['price'] <= self.balance:
                        result = await self.upgrade_card(upgrade['id'])
                        if result['status_code'] == HTTPStatus.OK:
                            result_data = result['data']
                            self.state = result_data["clickerUser"]
                        logging.info(self.log_prefix + MessageEnum.MSG_BUY_UPGRADE.format(**upgrade))
                        sleep(0.5)
                    else:
                        break
                else:
                    break
        else:
            await self.upgrades_list()

    async def claim_combo_reward(self) -> None:
        """ Получить награду, если собрано комбо """
        combo = self.upgrades.get('dailyCombo', {})
        upgrades = combo.get('upgradeIds', [])
        combo_cards = ", ".join(upgrades)
        logging.info(self.log_prefix + MessageEnum.MSG_CLAIMED_COMBO_CARDS.format(cards=combo_cards or '-'))
        if combo and len(upgrades) == 3:
            if combo.get('isClaimed') is False:

                async with self._session.request(method="POST", url=UrlsEnum.CLAIM_DAILY_COMBO) as response:
                    response.raise_for_status()
                    if response.status == HTTPStatus.OK:
                        response_state = await response.json()
                        self.state = response_state["clickerUser"]
                        logging.info(self.log_prefix + MessageEnum.MSG_COMBO_EARNED.format(coins=combo['bonusCoins']))
