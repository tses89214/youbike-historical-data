"""
This module contains the schema of tables,
and functions to transform schema into formats that meet other DB system.
"""
from typing import Dict

from google.cloud import bigquery


class Table:
    """
    Table schema.
    """

    def __init__(self, table_name: str, schema: Dict) -> None:
        """
        A base class of a table.

        Args:
            table_name (str): table name.
            schema (List[Dict]): {'column_name': 'data type', ... }
        """
        self.table_name = table_name
        self.schema = schema

    @property
    def columns(self):
        """
        get columns.
        """
        return list(self.schema.keys())

    def to_bq_schema(self):
        """
        to BigQuery Schema.
        """
        schema = []
        mappings = {
            'STRING': bigquery.enums.SqlTypeNames.STRING,
            'INT': bigquery.enums.SqlTypeNames.INT64,
            'DOUBLE': bigquery.enums.SqlTypeNames.FLOAT64,
            'DATETIME': bigquery.enums.SqlTypeNames.DATETIME
        }

        for key, value in self.schema.items():
            schema.append(
                bigquery.SchemaField(key, mappings[value])
            )
        return schema


sites = Table(
    table_name='sites',
    schema={
        'sno': 'STRING',
        'sna': 'STRING',
        'sarea': 'STRING',
        'latitude': 'DOUBLE',
        'longitude': 'DOUBLE',
        'ar': 'STRING',
        'sareaen': 'STRING',
        'aren': 'STRING',
        'act': 'STRING'
    }
)

site_md5 = Table(
    table_name='site_md5',
    schema={
        'md5': 'STRING'
    }
)


slots = Table(
    table_name='slots',
    schema={
        'sno': 'STRING',
        'total': 'INT',
        'available_rent_bikes': 'INT',
        'available_return_bikes': 'INT',
        'infoTime': 'DATETIME'
    }
)
