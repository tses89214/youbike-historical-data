import datetime

import pytest
import pandas as pd

from src.db_connector import BQConnector


@pytest.mark.bq_query_return_data(
    [
        {
            "query": "SELECT md5 FROM `ubike-crawler.ubike_data.site_md5` LIMIT 1 ",
            "table": {"columns": ["md5"], "rows": [["123"]]}
        }
    ]
)
def test_function_that_calls_bigquery(bq_client_mock):

    connector = BQConnector(bq_client_mock)
    assert connector.check_md5_for_update("123")

    connector.overwrite_sites(
        pd.DataFrame(
            {
                'sno': 'STRING',
                'sna': 'STRING',
                'tot': 123,
                'sarea': 'STRING',
                'lat': 1.23,
                'lng': 1.23,
                'ar': 'STRING',
                'sareaen': 'STRING',
                'aren': 'STRING',
                'act': 'STRING'
            }, index=[0])
    )

    connector.append_slots(
        pd.DataFrame(
            {
                'sno': 'STRING',
                'sbi': 0,
                'infoTime': datetime.datetime(2024, 1, 1, 0, 0, 0)
            }, index=[0])
    )
