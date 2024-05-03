import json

import requests_mock


from src.crawler import download_data, split_table


SAMPLE_DATA = """
[{
   "sno":"500101001",
   "sna":"YouBike2.0_捷運科技大樓站",
   "sarea":"大安區",
   "mday":"2024-05-03 23:52:18",
   "ar":"復興南路二段235號前",
   "sareaen":"Daan Dist.",
   "snaen":"YouBike2.0_MRT Technology Bldg. Sta.",
   "aren":"No.235， Sec. 2， Fuxing S. Rd.",
   "act":"1",
   "srcUpdateTime":"2024-05-03 23:53:24",
   "updateTime":"2024-05-03 23:53:52",
   "infoTime":"2024-05-03 23:52:18",
   "infoDate":"2024-05-03",
   "total":28,
   "available_rent_bikes":5,
   "latitude":25.02605,
   "longitude":121.5436,
   "available_return_bikes":23
}]
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
    assert all(col in site.columns for col in ['sno', 'sna', 'sarea',
                                               'latitude', 'longitude', 'ar', 'sareaen', 'aren', 'act'])

    # Assert slots table fields
    assert all(col in slots.columns for col in ['sno', 'total', 'available_rent_bikes',
                                                'available_return_bikes', 'infoTime'])

    # Assert length of site and slots tables
    assert len(site) == len(sample_data)
    assert len(slots) == len(sample_data)
