import logging
import random
import string
import threading
import time
import uuid
from datetime import datetime
from http import HTTPStatus
from typing import Dict, Union, List

import requests
from requests import Session

from config import MINI_GAMES

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s   %(message)s")


class CodeGenerator(Session):
    def __init__(self, game_name: str, key_count: int, name: str, **kwargs) -> None:
        super().__init__()
        self.game_name = game_name
        self.EVENTS_DELAY = 20  # секунд
        self.key_count = key_count
        self.name = name
        self.game: Dict = MINI_GAMES[self.game_name]

    @property
    def log_prefix(self) -> str:
        """ Префикс с именем пользователя для логирования """
        return f"[{self.name}]\t "

    @staticmethod
    def generate_client_id() -> str:
        """ Сгенерировать client_id """
        timestamp = int(datetime.now().timestamp() * 1000)
        random_numbers = ''.join(random.choices(string.digits, k=19))
        return f"{timestamp}-{random_numbers}"

    def sleep_with_random_delay(self) -> None:
        """ Случайная задержка """
        delay = self.EVENTS_DELAY * (random.random() / 3 + 1)
        time.sleep(delay)

    def get_client_token(self, client_id: str) -> str:
        """ Получить client_token """
        url = 'https://api.gamepromo.io/promo/login-client'
        payload = {
            "appToken": self.game["appToken"],
            "clientId": client_id,
            "clientOrigin": "deviceid"
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if response.status_code != HTTPStatus.OK:
            if data.get("error_code") == "TooManyIpRequest":
                raise Exception('Очень много запросов. Пожалуйста, подождите несколько минут и попробуйте еще раз.')
            else:
                raise Exception(data.get("error_message", 'Failed to log in'))

        return data["clientToken"]

    def emulate_progress(self, client_token: str) -> str:

        """ #todo
        :param client_token:
        """
        url = 'https://api.gamepromo.io/promo/register-event'
        payload = {
            "promoId": self.game["promoId"],
            "eventId": str(uuid.uuid4()),
            "eventOrigin": "undefined"
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {client_token}'
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        return data.get("hasCode", False)

    def generate_key(self, client_token: str) -> str:
        """  Сгенерировать ключ  """
        url = 'https://api.gamepromo.io/promo/create-code'
        payload = {"promoId": self.game["promoId"]}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {client_token}'
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if not response.ok:
            raise Exception(data.get("error_message", 'Failed to generate key'))

        return data["promoCode"]

    def generate_key_process(self) -> Union[str, None]:
        """ #todo """
        client_id = self.generate_client_id()
        try:
            client_token = self.get_client_token(client_id)
        except Exception as e:
            print(f"Failed to log in: {e}")
            return None

        for _ in range(7):
            self.sleep_with_random_delay()
            has_code = self.emulate_progress(client_token)
            if has_code:
                break

        try:
            key = self.generate_key(client_token)
            return key
        except Exception as e:
            print(f"Ошибка генерации ключа: {e}")
            return None

    def execute(self) -> List[str]:
        keys = []
        threads = []

        print(f"Началась генерация ключей для игры {self.game_name}...")

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


generator = CodeGenerator(game_name="Train Miner", key_count=4, name='М')
print(generator.execute())
