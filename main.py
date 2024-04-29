"""
Here is the main entrypoint of this project.
"""
import hashlib
import dotenv

from src.crawler import download_data, split_table
from src.db_connector import BQConnector


def main():
    """
    Main entrypoint.
    """
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

    # slots always update.
    bq_connector.append_slots(slots)


if __name__ == "__main__":
    main()
