from enum import StrEnum


class UrlsEnum(StrEnum):
    BASE_URL = "https://api.hamsterkombatgame.io/clicker"

    CLAIM_DAILY_CIPHER = BASE_URL + '/claim-daily-cipher',
    CLAIM_DAILY_COMBO = BASE_URL + '/claim-daily-combo',
    UPGRADES_FOR_BUY = BASE_URL + '/upgrades-for-buy',
    BOOSTS_FOR_BUY = BASE_URL + '/boosts-for-buy',
    BUY_UPGRADE = BASE_URL + '/buy-upgrade',
    APPLY_PROMO = BASE_URL + '/apply-promo',
    LIST_TASKS = BASE_URL + '/list-tasks',
    CHECK_TASK = BASE_URL + '/check-task',
    BUY_BOOST = BASE_URL + '/buy-boost',
    CONFIG = BASE_URL + '/config',
    SYNC = BASE_URL + '/sync',
    TAP = BASE_URL + '/tap',

    GAME_PROMO_BASE_URL = 'https://api.gamepromo.io/promo'
    LOGIN_CLIENT = GAME_PROMO_BASE_URL + '/login-client'
    REGISTER_EVENT = GAME_PROMO_BASE_URL + '/register-event'
    CREATE_CODE = GAME_PROMO_BASE_URL + '/create-code'


class MessageEnum(StrEnum):
    MSG_BUY_UPGRADE = "Прокачал: {name} : ур.{level} за {price} даст +{profitPerHourDelta}/час"
    MSG_SESSION_ERROR = "Ошибка во время выполнения запроса: {error}"
    MSG_COMBO_EARNED = "Получено вознаграждение за комбо: {coins}"
    MSG_BAD_RESPONSE = "Плохой ответ от сервера: {status} {text}"
    MSG_CLAIMED_COMBO_CARDS = "Полученные комбо карты: {cards}"
    MSG_TAP = "Тапнул на {taps_count} монет"
    MSG_SYNC = "Данные обновлены"
    MSG_SYNC_ERROR = "Ошибка при обновлении данных пользователя: {error}"

    MSG_CIPHER = "Новый шифр: {cipher}"
    MSG_CRYPTED_CIPHER = "Шифрованный шифр: {cipher}"

    MSG_TASK_COMPLETED = "Задание выполнено. Награда: {reward}"
    MSG_TASK_NOT_COMPLETED = "Задание не выполнено"

    MSG_SUCCESSFUL_PROMO_APPLY = "Ключ {code} успешно применён"
    MSG_GENERATE_KEYS_START = "Генерация ключей началась"
    MSG_GENERATE_KEYS_GAME = "Генерация ключей для {game}..."
    MSG_GENERATE_KEYS_END = "Генерация ключей завершена"
    MSG_UNSUCCESSFUL_PROMO_APPLY = "Ошибка применения ключа {code}"
    MSG_UNSUCCESSFUL_GETTING_CLIENT_TOKEN = "Неуспешное получение клиентского токена: {err}"
    MSG_UNSUCCESSFUL_GENERATE_KEY = "Ошибка генерации ключа: {err}"
