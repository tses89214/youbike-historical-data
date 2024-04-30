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
    today_slots = datetime.datetime.now().strftime('slots/%Y-%m-%d.csv')
    connector.read_slots().to_csv(f'data/{today_slots}', index=False)
    connector.clean_slots()


if __name__ == "__main__":
    main()
