from accounts import ACCOUNTS
from hamster_client import HamsterClient, sleep

clients = [HamsterClient(**options) for options in ACCOUNTS]


def main():
    while True:
        for client in clients:
            client.execute()
        print('-' * 120)
        sleep(60)


if __name__ == "__main__":
    main()
