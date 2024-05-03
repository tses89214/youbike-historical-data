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
                - sarea
                - latitude
                - longitude
                - ar
                - sareaen
                - snaen
                - aren
                - act

            Slots table fields:
                - sno
                - total
                - available_rent_bikes
                - available_return_bikes
                - infoTime

    """
    raw_table = pd.DataFrame(records)

    # At 2024/05/03 17:00, schema seems changed without notification. (#`Д´)ﾉ
    sites = raw_table[['sno', 'sna', 'sarea',
                      'latitude', 'longitude', 'ar', 'sareaen', 'aren', 'act']]

    slots = raw_table[['sno', 'total', 'available_rent_bikes',
                       'available_return_bikes', 'infoTime']]

    slots.loc[:, 'infoTime'] = pd.to_datetime(slots['infoTime'])

    logger.info("Split Table into Site and Slots two tables.")
    return sites, slots
