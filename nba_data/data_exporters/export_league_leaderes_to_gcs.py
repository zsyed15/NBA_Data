from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path
import os
import pyarrow as pa 
import pyarrow.parquet as pq

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/nba_data/secrets/g_key.json'
@data_exporter
def export_data_to_big_query(df: DataFrame, **kwargs) -> None:
    """
    Export league leaders to bigquery bucket, partitioned by season
    """
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = kwargs['cred_path']
    bucket_name = kwargs['bucket_name']
    table_name = kwargs['table_name']
    root_path = f'{bucket_name}/{table_name}'

    table = pa.Table.from_pandas(df)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
    table,
    root_path=root_path,
    partition_cols=['season'],
    filesystem = gcs)
