"""
    ACCOUNTS:
        name -> Имя аккаунта, отображаемое в логе
        token -> Brearer токен аккаунта
        proxies -> настройки прокси, "кто знает - тот поймет". Если не нужен прокси, лучше убрать
        buy_upgrades -> управление покупкой карточек.
            True -> Включено,
            False -> Выключено
        buy_decision_method -> метод покупки карточек (
            - price -> покупать самую дешевую
            - payback -> покупать ту, что быстрей всего окупится
            - profit -> покупать самую прибыльну
            - profitness -> покупать самую профитную (сколько добыча на каждый потраченный хома-рубль)
            )
"""

ACCOUNTS = [
    {
        "name": "m",
        "token": "1718258846672jWREfRSgL4yNjHPDli8Uxw7MMQHByewbJ4HMBWTUmA0CH1KhKNktAwff2QDC2xyE398277120",
        "buy_upgrades": False,
        "buy_decision_method": "profitness",
    },
    {
        "name": "t",
        "token": "17184376542545fCPKS5wju3SUKLnPzk6k3PwlEiDjZmm8uiZrLlI4qMTyxhph4GSfnoqE6ya592x1350814077",
        "buy_upgrades": False,
        "buy_decision_method": "profitness",
    },
]
