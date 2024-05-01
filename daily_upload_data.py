"""
This script used to export sites and slots data WEEKLY.
"""
import datetime
import dotenv
import os

from src.db_connector import BQConnector


def main():
    """
    export sites and slots data to csv weekly.
    """
    dotenv.load_dotenv(override=True)
    connector = BQConnector()

    os.makedirs('data/sites', exist_ok=True)
    os.makedirs('data/slots', exist_ok=True)

    connector.read_sites().to_csv('data/sites/sites.csv', index=False)

    date = datetime.datetime.now() - datetime.timedelta(days=2)
    slots_filename = date.strftime('data/slots/%Y-%m-%d.csv')
    connector.read_slots().to_csv(slots_filename, index=False)
    connector.clean_slots()


if __name__ == "__main__":
    main()
