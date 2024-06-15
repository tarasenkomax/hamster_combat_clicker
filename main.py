from random import choice

from config import ACCOUNTS
from hamster_client import HamsterClient, logging, sleep

clients = [HamsterClient(**options) for options in ACCOUNTS]


def main():
    while True:
        for client in clients:
            print("-" * 150)
            client.sync()
            client.claim_daily_cipher()
            client.tap()
            client.buy_upgrades()
            client.check_task()
            client.claim_combo_reward()
            if client.is_taps_boost_available:
                client.boost()
            logging.info(client.log_prefix + " ".join(f"{k}: {v} |" for k, v in client.stats.items()))
            print("-" * 150)
            sleep(choice(range(1, 10)))
        sleep(60)


if __name__ == "__main__":
    main()
