import asyncio

from accounts import ACCOUNTS
from client import HamsterClient, logging, sleep


async def main():
    accounts = [HamsterClient(**options) for options in ACCOUNTS]
    while True:
        for account in accounts:
            await account.sync()
            await account.claim_daily_cipher()
            await account.tap()
            await account.buy_upgrades()
            await account.check_task()
            await account.claim_combo_reward()
            if await account.is_taps_boost_available:
                await account.apply_boost()
            logging.info(account.log_prefix + " ".join(f"{k}: {v} |" for k, v in account.stats.items()))
        sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
