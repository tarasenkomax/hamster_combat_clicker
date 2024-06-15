from random import choice

from accounts import ACCOUNTS
from hamster_client import HamsterClient, logging, sleep

clients = [HamsterClient(**options) for options in ACCOUNTS]


def main():
    while True:
        for client in clients:
            client.sync()
            client.claim_daily_cipher()
            client.tap()
            client.buy_upgrades()
            client.check_task()
            client.claim_combo_reward()
            if client.is_taps_boost_available:
                client.apply_boost()
            logging.info(client.log_prefix + " ".join(f"{k}: {v} |" for k, v in client.stats.items()))
            sleep(0.5)
            print(' ')
        print('-' * 120)
        sleep(60)


if __name__ == "__main__":
    main()
