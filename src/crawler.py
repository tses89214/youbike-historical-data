"""
Some functions to download data from ubike api. 
"""
from typing import List, Dict

import requests
import pandas as pd

from src.logger import logger


def download_data():
    """
    Download data from ubike api.

    Returns:
        data: List of json(records).
    """
    url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    data = requests.get(url, timeout=60).json()

    logger.info("Get data from API, len = %s", str(len(data)))
    return data


def split_table(records: List[Dict]):
    """
    Split Table into Site and Slots two tables.

    Args:
        records: List of Dict. The raw data get from API.

    Returns:
        (Sites, Slots):
            Sites table fields:
                - sno
                - sna
                - tot
                - sarea
                - lat
                - lng
                - ar
                - sareaen
                - snaen
                - aren
                - act

            Slots table fields:
                - sno
                - sbi
                - infoTime

    """
    raw_table = pd.DataFrame(records)

    # At 2024/05/03, schema seems changed without notification.
    rename_columns = {
        "total": "tot",
        "latitude": "lat",
        "longitude": "lng",
        "sbi": "available_rent_bikes",
    }
    raw_table = raw_table.rename(rename_columns, errors='ignore')

    sites = raw_table[['sno', 'sna', 'tot', 'sarea',
                      'lat', 'lng', 'ar', 'sareaen', 'aren', 'act']]
    slots = raw_table[['sno', 'sbi', 'infoTime']]
    slots.loc[:, 'infoTime'] = pd.to_datetime(slots['infoTime'])

    logger.info("Split Table into Site and Slots two tables.")
    return sites, slots
