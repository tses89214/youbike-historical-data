"""
Here is the main entrypoint of this project.
"""
import hashlib
import traceback

import dotenv

from src.crawler import download_data, split_table
from src.db_connector import BQConnector
from src.alarm import TGBot


def main():
    """
    Main entrypoint.
    """
    try:
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

        # slots always update.
        bq_connector.append_slots(slots)

    # pylint:disable=broad-exception-caught
    except Exception:
        dotenv.load_dotenv(override=True)
        bot = TGBot()
        bot.send_message(traceback.format_exc())


if __name__ == "__main__":
    main()
