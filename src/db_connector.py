"""
This modules contains connector used to Connect to databases.
Currently we only has BigQuery Connector(BQConnector).
"""
from google.cloud import bigquery
import pandas as pd

from src.table import sites, slots, site_md5
from src.logger import logger


class BQConnector:
    """
    This class is used to Connect to BigQuery,
    To keep things simple, store and write logic are included in this script.
    """

    def __init__(self, client: bigquery.Client = None) -> None:
        self._client = bigquery.Client() if client is None else client
        logger.info("Initializing database connector.")

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

        logger.info(
            "Get md5 from db: %s, md5 from new data: %s",
            current_md5, site_data_md5)
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
        logger.info("Overwrite Sites table.")
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
        logger.info("Overwrite Sites md5 table.")
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
        logger.info("Append data into Slots table.")
        return job.result()

    def read_sites(self) -> pd.DataFrame:
        """
        Read the whole sites table.

        Returns:
            bool: whether md5 is same.
        """
        query = 'SELECT * FROM `ubike-crawler.ubike_data.sites`'
        query_job = self._client.query(query)
        logger.info("Read the whole sites table.")
        return query_job.to_dataframe()

    def read_slots(self, date: str) -> pd.DataFrame:
        """
        Read the slots table of specific time range.

        Args:
            date: str. The date want to export.

        Returns:
            bool: whether md5 is same.
        """
        query = f"""
            SELECT distinct * FROM `ubike-crawler.ubike_data.slots`
            WHERE DATE(infoTime) = '{date}'
        """
        query_job = self._client.query(query)
        logger.info("Read the slots table, range: %s", date)
        return query_job.to_dataframe()

    def clean_slots(self, date: str):
        """
        Clean past data from slots table.

        Args:
            date: str. The date want to export.

        """
        query = f"""
            DELETE FROM `ubike-crawler.ubike_data.slots`
            WHERE DATE(infoTime) = '{date}'
        """
        delete_job = self._client.query(query)
        logger.info("Clean past data from slots table, range: %s", date)
        return delete_job.result()

    def get_new_data_flag(self):
        """
        Get new data flag from site_md5 table.
        """
        query = 'SELECT new_data_flag FROM `ubike-crawler.ubike_data.site_md5` LIMIT 1 '
        query_job = self._client.query(query)
        rows = query_job.result()
        for row in rows:
            new_data_flag = row['new_data_flag']

        logger.info("Get new data flag: %s", str(new_data_flag))
        return new_data_flag

    def set_new_data_flag(self, flag: bool):
        """
        Set new data flag of site_md5 table.
        """
        query = f"""UPDATE `ubike-crawler.ubike_data.site_md5` 
                    SET new_data_flag = {flag} WHERE 1=1"""
        update_job = self._client.query(query)
        update_job.result()
        logger.info("Set new data flag: %s", str(flag))
