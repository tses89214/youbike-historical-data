from google.cloud import bigquery

from src.table import Table


def test_table():
    t = Table(
        table_name='test_table',
        schema={'col_a': 'STRING', 'col_b': 'INT'}
    )

    assert t.columns == ['col_a', 'col_b']
    assert t.to_bq_schema() == [
        bigquery.SchemaField('col_a', bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField('col_b', bigquery.enums.SqlTypeNames.INT64),
    ]
