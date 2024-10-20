"""
Here is the main entrypoint of this project.
"""
import hashlib
import traceback

import dotenv

from src.crawler import download_data, split_table
from src.db_connector import BQConnector
from src.alarm import TGBot
from src.logger import logger


def main():
    """
    Main entrypoint.
    """
    try:
        logger.info("Starting download execution.")
        dotenv.load_dotenv(override=True)

        bq_connector = BQConnector()

        records = download_data()
        sites, slots = split_table(records)

        # generate current md5 for check.
        m = hashlib.md5()
        m.update(sites.to_string().encode())
        current_md5 = m.hexdigest()
        md5_check_result = bq_connector.check_md5_for_update(current_md5)

        if md5_check_result is False:
            bq_connector.overwrite_sites(sites)
            bq_connector.overwrite_site_md5(current_md5)
            bq_connector.set_new_data_flag(True)
            logger.info("Upload sites table.")

        # slots always update.
        bq_connector.append_slots(slots)
        logger.info("Upload slots table.")

    # TODO: currently we catch all exception, fix it later.
    # pylint:disable=broad-exception-caught
    except Exception:
        dotenv.load_dotenv(override=True)
        bot = TGBot()
        bot.send_message(traceback.format_exc())
        logger.error("Meet Exception:", exc_info=True)


if __name__ == "__main__":
    main()
