"""
This modules contains connector used to Connect to databases.
Currently we only has BigQuery Connector(BQConnector).
"""
from google.cloud import bigquery
import pandas as pd

from src.table import sites, slots, site_md5


class BQConnector:
    """
    This class is used to Connect to BigQuery,
    To keep things simple, store and write logic are included in this script.
    """

    def __init__(self, client: bigquery.Client = None) -> None:
        self._client = bigquery.Client() if client is None else client

    def check_md5_for_update(self, site_data_md5: str) -> bool:
        """
        Check is md5 same or not.

        Args:
            site_data_md5: str. the md5 of site data.

        Returns:
            bool: whether md5 is same.
        """
        query = 'SELECT md5 FROM `ubike-crawler.ubike_data.site_md5` LIMIT 1 '
        query_job = self._client.query(query)
        rows = query_job.result()
        for row in rows:
            current_md5 = row['md5']

        return current_md5 == site_data_md5

    def overwrite_sites(self, sites_data: pd.DataFrame):
        """
        Overwrite sites table.

        Args:
            sites_data (pd.DataFrame): sites data.

        Returns:
            job results.
        """
        table_id = 'ubike-crawler.ubike_data.sites'
        job_config = bigquery.LoadJobConfig(
            schema=sites.to_bq_schema(),
            write_disposition='WRITE_TRUNCATE'
        )
        job = self._client.load_table_from_dataframe(
            sites_data, table_id, job_config=job_config
        )
        return job.result()

    def overwrite_site_md5(self, site_md5_data: str):
        """
        Overwrite site_md5 table.

        Args:
            site_md5 (str): site_md5.

        Returns:
            job results.
        """
        table_id = 'ubike-crawler.ubike_data.site_md5'
        job_config = bigquery.LoadJobConfig(
            schema=site_md5.to_bq_schema(),
            write_disposition='WRITE_TRUNCATE'
        )
        job = self._client.load_table_from_dataframe(
            pd.DataFrame({'md5': site_md5_data}, index=[0]),
            table_id,
            job_config=job_config
        )
        return job.result()

    def append_slots(self, slots_data: pd.DataFrame):
        """
        Append sites table.

        Args:
            slots_data (pd.DataFrame): slots data.

        Returns:
            job results.
        """
        table_id = 'ubike-crawler.ubike_data.slots'
        job_config = bigquery.LoadJobConfig(
            schema=slots.to_bq_schema(),
            write_disposition='WRITE_APPEND'
        )
        job = self._client.load_table_from_dataframe(
            slots_data, table_id, job_config=job_config
        )
        return job.result()

    def read_sites(self) -> pd.DataFrame:
        """
        Read the whole sites table.

        Returns:
            bool: whether md5 is same.
        """
        query = 'SELECT * FROM `ubike-crawler.ubike_data.sites`'
        query_job = self._client.query(query)
        return query_job.to_dataframe()

    def read_slots(self) -> pd.DataFrame:
        """
        Read the slots table of specific time range.

        Returns:
            bool: whether md5 is same.
        """
        query = """
            SELECT distinct * FROM `ubike-crawler.ubike_data.slots`
            WHERE DATE(infoTime) BETWEEN 
                DATE_SUB(CURRENT_DATE(), INTERVAL 8 DAY) 
                AND 
                DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
        """
        query_job = self._client.query(query)
        return query_job.to_dataframe()

    def clean_slots(self):
        """
        Clean last week data from slots table.
        """
        query = """
            DELETE FROM `ubike-crawler.ubike_data.slots`
            WHERE DATE(infoTime) BETWEEN 
                DATE_SUB(CURRENT_DATE(), INTERVAL 8 DAY) 
                AND 
                DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
        """
        delete_job = self._client.query(query)
        delete_job.result()
