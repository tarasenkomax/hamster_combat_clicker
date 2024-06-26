"""
    ACCOUNTS:
        name -> Имя аккаунта, отображаемое в логах
        token -> Brearer токен аккаунта
        buy_upgrades -> Покупка карточек.
            True -> Включено,
            False -> Выключено
        buy_decision_method -> метод покупки карточек.
            - price -> покупать самую дешевую
            - payback -> покупать ту, что быстрей всего окупится
            - profit -> покупать самую прибыльну
            - profitness -> покупать самую профитную (сколько добыча на каждый потраченный хома-рубль)
"""

ACCOUNTS = [
    {
        "name": "М",
        "token": "1718258846672jWREfRSgL4yNjHPDli8Uxw7MMQHByewbJ4HMBWTUmA0CH1KhKNktAwff2QDC2xyE398277120",
        "buy_upgrades": True,
        "buy_decision_method": "profitness",
    },
    {
        "name": "Т",
        "token": "17184376542545fCPKS5wju3SUKLnPzk6k3PwlEiDjZmm8uiZrLlI4qMTyxhph4GSfnoqE6ya592x1350814077",
        "buy_upgrades": True,
        "buy_decision_method": "profitness",
    },
]
