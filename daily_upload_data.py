"""
This script used to export sites and slots data daily.
"""
import datetime
import os
import traceback

import dotenv

from src.db_connector import BQConnector
from src.alarm import TGBot
from src.logger import logger


def main():
    """
    export sites and slots data to csv daily.
    """
    try:
        dotenv.load_dotenv(override=True)
        connector = BQConnector()

        os.makedirs('data/sites', exist_ok=True)
        os.makedirs('data/slots', exist_ok=True)

        target_date = datetime.datetime.now() - datetime.timedelta(days=1)
        logger.info("Daily upload data, range: %s",
                    target_date.strftime("%Y-%m-%d"))

        if connector.get_new_data_flag():
            connector.read_sites() \
                .to_csv(f'data/sites/{target_date.strftime("%Y-%m-%d")}.csv', index=False)
            connector.set_new_data_flag(flag=False)
            logger.info("Upload new sites table.")

        connector.read_slots(date=target_date.strftime('%Y-%m-%d')) \
            .to_csv(f'data/slots/{target_date.strftime("%Y-%m-%d")}.csv', index=False)
        connector.clean_slots(date=target_date.strftime('%Y-%m-%d'))

    # TODO: currently we catch all exception, fix it later.
    # pylint:disable=broad-exception-caught
    except Exception:
        dotenv.load_dotenv(override=True)
        bot = TGBot()
        bot.send_message(traceback.format_exc())
        logger.error("Meet Exception:", exc_info=True)


if __name__ == "__main__":
    main()
