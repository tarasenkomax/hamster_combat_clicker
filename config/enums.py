from enum import StrEnum


class UrlsEnum(StrEnum):
    BASE_URL = "https://api.hamsterkombatgame.io/clicker"

    CLAIM_DAILY_CIPHER = BASE_URL + '/claim-daily-cipher',
    CLAIM_DAILY_COMBO = BASE_URL + '/claim-daily-combo',
    UPGRADES_FOR_BUY = BASE_URL + '/upgrades-for-buy',
    BOOSTS_FOR_BUY = BASE_URL + '/boosts-for-buy',
    BUY_UPGRADE = BASE_URL + '/buy-upgrade',
    APPLY_PROMO = BASE_URL + '/apply-promo',
    GET_PROMOS = BASE_URL + '/get-promos',
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
    MSG_COMBO_EARNED = "Получено вознаграждение за комбо: {coins}"
    MSG_CLAIMED_COMBO_CARDS = "Полученные комбо карты: {cards}"
    MSG_TAP = "Тапнул на {taps_count} монет"
    MSG_SYNC = "Данные обновлены"
    MSG_SESSION_ERROR = "Ошибка во время выполнения запроса: {error}"
    MSG_BAD_RESPONSE = "Плохой ответ от сервера: {status} {text}"
    MSG_SYNC_ERROR = "Ошибка при обновлении данных пользователя: {error}"

    MSG_CIPHER = "Новый шифр: {cipher}"
    MSG_ENCRYPTED_CIPHER = "Шифрованный шифр: {cipher}"

    MSG_YOUTUBE_TASK_COMPLETED = "Youtube видео просмотрено. Награда получена"
    MSG_YOUTUBE_TASK_NOT_COMPLETED = "Youtube видео не просмотрено"

    MSG_SUCCESSFUL_PROMO_APPLY = "Ключ {code} успешно применён"
    MSG_NEW_GAME_FOUND = "Найдена новая игра с promo_id = {promo_id}"
    MSG_NEW_GAME_NOT_FOUND = "Игра с promo_id = {promo_id} не найдена в списке игр."
    MSG_GENERATE_KEYS_GAME = "Генерация ключей для {game}..."
    MSG_UNSUCCESSFUL_PROMO_APPLY = "Ошибка применения ключа {code}"
    MSG_UNSUCCESSFUL_EMULATE_PROGRESS = "Ошибка эмулирования игрового процесса {err}"
    MSG_UNSUCCESSFUL_GETTING_CLIENT_TOKEN = "Неуспешное получение клиентского токена: {err}"
    MSG_UNHANDLED_ERROR = "Необработанная ошибка при генерации ключа: {err}"
    MSG_UNSUCCESSFUL_GENERATE_KEY = "Ошибка генерации ключа: {err}"
