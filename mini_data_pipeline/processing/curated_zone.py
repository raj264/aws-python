"""Module: curated_zone.py
Handles writing Parquet to the curated zone and registering Athena tables."""
import boto3
import pyarrow.parquet as pq
import pyarrow as pa

def write_curated_parquet(bucket: str, enriched_key: str, curated_prefix: str, timestamp: str) -> str:
    """Read JSON, convert to Parquet, store under curated prefix.
    :return: S3 path of Parquet files"""
    import s3fs
    fs = s3fs.S3FileSystem()
    input_path = f's3://{bucket}/{enriched_key}'
    table = pq.read_table(input_path, filesystem=fs)
    out_prefix = f'{curated_prefix}{timestamp}/'
    out_path = f's3://{bucket}/{out_prefix}'
    pq.write_to_dataset(table, root_path=out_path, filesystem=fs, partition_cols=['year','month'])
    return out_path

def register_athena_table(bucket: str, parquet_path: str, database: str, table: str):
    """Create or update a Glue Data Catalog table over Parquet data so it's queryable from Athena."""
    glue = boto3.client('glue')
    table_input = {
        'Name': table,
        'StorageDescriptor': {
            'Location': parquet_path,
            'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
            'SerdeInfo': {
                'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe',
            },
        },
        'PartitionKeys': [
            {'Name': 'year', 'Type': 'string'},
            {'Name': 'month', 'Type': 'string'},
        ],
        'TableType': 'EXTERNAL_TABLE',
    }

    try:
        glue.create_table(DatabaseName=database, TableInput=table_input)
    except glue.exceptions.AlreadyExistsException:
        glue.update_table(DatabaseName=database, TableInput=table_input)
