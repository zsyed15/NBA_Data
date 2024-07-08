import pyarrow as pa 
import pyarrow.parquet as pq
import os
from pandas import DataFrame


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/nba_data/secrets/g_key.json'

@data_exporter
def export_data(data, *args, **kwargs):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = kwargs['cred_path']
    bucket_name = kwargs['bucket_name']
    table_name = kwargs['table_name']
    root_path = f'{bucket_name}/{table_name}'

    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
    table,
    root_path=root_path,
    partition_cols=['team'],
    filesystem = gcs)


