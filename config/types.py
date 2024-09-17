from typing import List, Literal, TypedDict
from uuid import UUID


class Account(TypedDict):
    """
    name(str) -> Имя аккаунта, отображаемое в логах
    token -> Brearer токен аккаунта
    buy_upgrades(bool) -> Покупка карточек
    buy_decision_method(str) -> метод покупки карточек
        - price -> покупать самую дешевую
        - payback -> покупать ту, что быстрей всего окупится
        - profit -> покупать самую прибыльну
        - profitability -> покупать самую профитную (сколько добыча на каждую потраченную монетку)
    """
    name: str
    token: str
    buy_upgrades: bool
    buy_decision_method: Literal["price"] | Literal["payback"] | Literal["profit"] | Literal["profitability"]


class Boost(TypedDict, total=False):
    id: str
    price: int
    earnPerTap: int
    maxTaps: int
    maxLevel: int
    cooldownSeconds: int
    level: int
    maxTapsDelta: int
    earnPerTapDelta: int


class Boosts(TypedDict):
    boostsForBuy: List[Boost]


class MiniGame(TypedDict):
    name: str
    app_token: str
    events_delay: int
    attempts_number: int


class CiperData(TypedDict):
    cipher: str
    bonusCoins: int
    isClaimed: bool
    remainSeconds: int


class PromoState(TypedDict):
    promoId: UUID
    receiveKeysToday: int
    receiveKeysRefreshSec: int


class PromoInfo(TypedDict):
    promoId: UUID
    keysPerDay: int
    title: str
    rewardType: Literal["keys"] | Literal["coins"]
