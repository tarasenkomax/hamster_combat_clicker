from accounts import ACCOUNTS
from hamster_client import HamsterClient, sleep

clients = [HamsterClient(**options) for options in ACCOUNTS]


def main():
    while True:
        for client in clients:
            client.sync()
            client.apply_all_codes()
            client.claim_daily_cipher()
            client.tap()
            client.buy_upgrades()
            client.check_task()
            client.execute_youtube_tasks()
            client.claim_combo_reward()
            client.apply_boost()
            client.log_stats()
            sleep(0.5)
            print(' ')
        print('-' * 120)
        sleep(60)


if __name__ == "__main__":
    main()
