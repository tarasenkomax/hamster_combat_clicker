import logging
import random
import string
import threading
import time
import uuid
from datetime import datetime
from http import HTTPStatus
from typing import List, Union

from requests import Session

from config.enums import MessageEnum, UrlsEnum
from config.mini_games import MINI_GAMES
from config.types import MiniGame

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s   %(message)s")


class CodeGenerator(Session):
    def __init__(self, promo_id: uuid.UUID, key_count: int, account_name: str) -> None:
        super().__init__()
        self.game: MiniGame = MINI_GAMES[promo_id]
        self.promo_id: uuid.UUID = promo_id
        self.key_count: int = key_count
        self.account_name: str = account_name

    @property
    def log_prefix(self) -> str:
        """ Префикс с именем пользователя для логирования """
        return f"[{self.account_name}]\t "

    @staticmethod
    def generate_client_id() -> str:
        """ Сгенерировать client_id """
        timestamp = int(datetime.now().timestamp() * 1000)
        random_numbers = ''.join(random.choices(string.digits, k=19))
        return f"{timestamp}-{random_numbers}"

    def sleep_with_random_delay(self) -> None:
        """ Случайная задержка """
        delay = self.game['events_delay'] * (random.random() / 3 + 1)
        time.sleep(delay)

    def get_client_token(self, client_id: str) -> str:
        """ Получить client_token """

        response = self.post(
            url=UrlsEnum.LOGIN_CLIENT,
            json={
                "appToken": self.game["app_token"],
                "clientId": client_id,
                "clientOrigin": "deviceid",
            },
            headers={
                'Content-Type': 'application/json',
            }
        )
        data = response.json()

        if response.status_code != HTTPStatus.OK:
            if data.get("error_code") == "TooManyIpRequest":
                raise Exception('Очень много запросов. Пожалуйста, подождите несколько минут и попробуйте еще раз.')
            else:
                raise Exception(data.get("error_message", 'Failed to log in'))

        return data["clientToken"]

    def emulate_progress(self, client_token: str) -> str:

        response = self.post(
            url=UrlsEnum.REGISTER_EVENT,
            json={
                "promoId": self.promo_id,
                "eventId": str(uuid.uuid4()),
                "eventOrigin": "undefined",
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {client_token}',
            },
        )
        data = response.json()
        return data.get("hasCode", False)

    def generate_key(self, client_token: str) -> str:
        """ Сгенерировать ключ """
        response = self.post(
            url=UrlsEnum.CREATE_CODE,
            json={
                "promoId": self.promo_id,
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {client_token}',
            },
        )
        data = response.json()

        if not response.ok:
            raise Exception(data.get("error_message", 'Не удалось сгенерировать ключ'))

        return data["promoCode"]

    def generate_key_process(self) -> Union[str, None]:  # noqa C901
        client_id = self.generate_client_id()

        try:
            client_token = self.get_client_token(client_id)
        except Exception as err:
            logging.error(self.log_prefix + MessageEnum.MSG_UNSUCCESSFUL_GETTING_CLIENT_TOKEN.format(err=err))
            return None

        for _ in range(self.game['attempts_number']):
            try:
                self.sleep_with_random_delay()
                has_code = self.emulate_progress(client_token)
                if has_code:
                    break
            except Exception as err:
                logging.error(self.log_prefix + MessageEnum.MSG_UNSUCCESSFUL_EMULATE_PROGRESS.format(err=err))

        try:
            key = self.generate_key(client_token)
            return key
        except Exception as err:
            logging.error(self.log_prefix + MessageEnum.MSG_UNSUCCESSFUL_GENERATE_KEY.format(err=err))
            return None

    def execute(self) -> List[str]:
        keys = []
        threads = []

        logging.info(self.log_prefix + MessageEnum.MSG_GENERATE_KEYS_GAME.format(game=self.game['name']))

        def worker():
            key = self.generate_key_process()
            if key:
                keys.append(key)

        for _ in range(self.key_count):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        return keys
