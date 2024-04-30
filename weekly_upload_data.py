"""
This script used to export sites and slots data WEEKLY.
"""
import datetime

from src.db_connector import BQConnector


def main():
    """
    export sites and slots data to csv weekly.
    """
    connector = BQConnector()
    connector.read_sites().to_csv('data/sites/sites.csv')

    today_slots = datetime.datetime.strftime('slots/%Y-%m-%d.csv')
    connector.read_slots().to_csv(f'data/{today_slots}')

if __name__ == "__main__":
    main()
    