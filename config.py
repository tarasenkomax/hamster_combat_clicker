"""
    FEATURES:
        1. buy_upgrades -> управление покупкой карточек.
            True -> Включено,
            False -> Выключено
        2. buy_decision_method -> метод покупки карточек (
            - price -> покупать самую дешевую
            - payback -> покупать ту, что быстрей всего окупится
            - profit -> покупать самую прибыльну
            - profitness -> покупать самую профитную (сколько добыча на каждый потраченный хома-рубль)
            )
        3. delay_between_attempts -> Задержка между заходами в секундах

    ACCOUNTS:
        name -> Название аккаунта. Так он будет виден в логе
        token -> токен аккаунта
        proxies -> настройки прокси, "кто знает - тот поймет". Если не нужен прокси, лучше убрать
        buy_upgrades -> Описано в FEATURES, можно указать для каждого аккаунта отдельно
        buy_decision_method -> Описано в FEATURES, можно указать для каждого аккаунта отдельно
"""

FEATURES = {
    "buy_upgrades": True,
    "buy_decision_method": "payback",
    "delay_between_attempts": 60 * 1,
}

ACCOUNTS = [
    {
        "name": "m",
        "token": "1718258846672jWREfRSgL4yNjHPDli8Uxw7MMQHByewbJ4HMBWTUmA0CH1KhKNktAwff2QDC2xyE398277120",
        "buy_upgrades": True,
        "buy_decision_method": "profitness",
    },
    {
        "name": "t",
        "token": "17184376542545fCPKS5wju3SUKLnPzk6k3PwlEiDjZmm8uiZrLlI4qMTyxhph4GSfnoqE6ya592x1350814077",
        "buy_upgrades": True,
        "buy_decision_method": "profitness",
    },
]
