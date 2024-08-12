from enum import StrEnum


class UrlsEnum(StrEnum):
    BASE_URL = "https://api.hamsterkombatgame.io/clicker"
    CHECK_IP = 'https://httpbin.org/ip'

    CLAIM_DAILY_CIPHER = BASE_URL + '/claim-daily-cipher',
    CLAIM_DAILY_COMBO = BASE_URL + '/claim-daily-combo',
    UPGRADES_FOR_BUY = BASE_URL + '/upgrades-for-buy',
    BOOSTS_FOR_BUY = BASE_URL + '/boosts-for-buy',
    BUY_UPGRADE = BASE_URL + '/buy-upgrade',
    LIST_TASKS = BASE_URL + '/list-tasks',
    CHECK_TASK = BASE_URL + '/check-task',
    BUY_BOOST = BASE_URL + '/buy-boost',
    CONFIG = BASE_URL + '/config',
    SYNC = BASE_URL + '/sync',
    TAP = BASE_URL + '/tap',


class MessageEnum(StrEnum):
    MSG_BUY_UPGRADE = "Прокачал: {name} : ур.{level} за {price} даст +{profitPerHourDelta}/час"
    MSG_SESSION_ERROR = "Ошибка во время выполнения запроса: {error}"
    MSG_COMBO_EARNED = "Получено вознаграждение за комбо: {coins}"
    MSG_BAD_RESPONSE = "Плохой ответ от сервера: {status} {text}"
    MSG_CLAIMED_COMBO_CARDS = "Полученные комбо карты: {cards}"
    MSG_CRYPTED_CIPHER = "Шифрованный шифр: {cipher}"
    MSG_TAP = "Тапнул на {taps_count} монет"
    MSG_CIPHER = "Новый шифр: {cipher}"
    MSG_SYNC = "Данные обновлены"
    MSG_SYNC_ERROR = "Ошибка при обновлении данных пользователя: {error}"
    MSG_TASK_COMPLETED = "Задание выполнено. Награда: {reward}"
    MSG_TASK_NOT_COMPLETED = "Задание не выполнено"
