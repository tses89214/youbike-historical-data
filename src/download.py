import requests


def download_data():
    url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    data = requests.get(url, timeout=60).json()

    return data
