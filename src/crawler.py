"""
Some functions to download data from ubike api. 
"""
from typing import List, Dict

import requests
import pandas as pd


def download_data():
    """
    Download data from ubike api.

    Returns:
        data: List of json(records).
    """
    url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    data = requests.get(url, timeout=60).json()
    return data


def split_table(records: List[Dict]):
    """
    Split Table into Site and Slots two tables.

    Args:
        records: List of Dict. The raw data get from API.

    Returns:
        (Site, Slots):
            Site table fields:
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
    site = raw_table[['sno', 'sna', 'tot', 'sarea',
                      'lat', 'lng', 'ar', 'sareaen', 'aren', 'act']]
    slots = raw_table[['sno', 'sbi', 'infoTime']]

    return site, slots
