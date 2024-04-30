import json

import requests_mock


from src.crawler import download_data, split_table


SAMPLE_DATA = """
[{"sno": "500101001",
  "sna": "YouBike2.0_捷運科技大樓站",
  "tot": 28,
  "sbi": 2,
  "sarea": "大安區",
  "mday": "2024-04-29 08:18:19",
  "lat": 25.02605,
  "lng": 121.5436,
  "ar": "復興南路二段235號前",
  "sareaen": "Daan Dist.",
  "snaen": "YouBike2.0_MRT Technology Bldg. Sta.",
  "aren": "No.235， Sec. 2， Fuxing S. Rd.",
  "bemp": 26,
  "act": "1",
  "srcUpdateTime": "2024-04-29 08:18:25",
  "updateTime": "2024-04-29 08:18:27",
  "infoTime": "2024-04-29 08:18:19",
  "infoDate": "2024-04-29"}]
"""


def test_download_data():
    with requests_mock.Mocker() as m:
        m.get(
            'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json',
            text=SAMPLE_DATA)

        data = download_data()
        assert isinstance(data, list)
        assert len(data) > 0


def test_split_table():
    # Test if splitting table works correctly
    sample_data = json.loads(SAMPLE_DATA)
    site, slots = split_table(sample_data)

    # Assert site table fields
    assert all(col in site.columns for col in [
               'sno', 'sna', 'tot', 'sarea', 'lat', 'lng', 'ar', 'sareaen', 'aren', 'act'])

    # Assert slots table fields
    assert all(col in slots.columns for col in ['sno', 'sbi', 'infoTime'])

    # Assert length of site and slots tables
    assert len(site) == len(sample_data)
    assert len(slots) == len(sample_data)
