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
    export sites and slots data to csv weekly.
    """
    try:
        dotenv.load_dotenv(override=True)
        connector = BQConnector()

        os.makedirs('data/sites', exist_ok=True)
        os.makedirs('data/slots', exist_ok=True)

        connector.read_sites().to_csv('data/sites/sites.csv', index=False)

        target_date = datetime.datetime.now() - datetime.timedelta(days=1)
        slots_filename = target_date.strftime('data/slots/%Y-%m-%d.csv')
        connector.read_slots(
            date=target_date.strftime('%Y-%m-%d')
        ).to_csv(slots_filename, index=False)
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
