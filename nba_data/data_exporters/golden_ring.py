import os
import pyarrow as pa
import pyarrow.parquet as pq

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/nba_data/secrets/g_key.json'

bucket_name = 'nba-data-account'
table_name = 'nba_player_names'
project_id = 'delta-cortex-327423'
root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to GCS
    """
    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()
    pq.write_to_dataset(
            table,
            root_path,
            partition_cols=['is_active'],
            filesystem=gcs
        )
 


