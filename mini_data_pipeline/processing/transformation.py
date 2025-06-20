"""Module: transformation.py
Class-based PySpark job for transformation and enrichment of staged data."""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month
import boto3

class TransformationJob:
    """Handles type casting, derived fields, lookup joins, deduplication, and write."""
    def __init__(self, raw_bucket, staging_prefix, enriched_prefix,
                 lookup_jdbc_url, lookup_table):
        self.raw_bucket = raw_bucket
        self.staging_prefix = staging_prefix
        self.enriched_prefix = enriched_prefix
        self.lookup_jdbc_url = lookup_jdbc_url
        self.lookup_table = lookup_table
        self.spark = SparkSession.builder.appName('transform_enrich').getOrCreate()

    def normalize_casts(self, df):
        """Cast id to string and timestamp to timestamp type."""
        try:
            return df.withColumn('id', col('id').cast('string')) \
                     .withColumn('timestamp', col('timestamp').cast('timestamp'))
        except Exception as e:
            raise RuntimeError(f"Error normalizing types: {e}")

    def derive_fields(self, df):
        """Add 'year' and 'month' columns from timestamp."""
        try:
            return df.withColumn('year', year(col('timestamp'))) \
                     .withColumn('month', month(col('timestamp')))
        except Exception as e:
            raise RuntimeError(f"Error deriving fields: {e}")

    def lookup_enrich(self, df):
        """Join with lookup table via JDBC to enrich records."""
        try:
            lookup_df = self.spark.read.format('jdbc') \
                .option('url', self.lookup_jdbc_url) \
                .option('dbtable', self.lookup_table) \
                .option('driver', 'org.postgresql.Driver') \
                .load()
            return df.join(lookup_df, on='id', how='left')
        except Exception as e:
            raise RuntimeError(f"Error during lookup join: {e}")

    def dedup_and_write(self, df, timestamp):
        """Deduplicate and write partitioned JSON to S3."""
        try:
            out_path = f's3://{self.raw_bucket}/{self.enriched_prefix}year={df.first()["year"]}/month={df.first()["month"]}/{timestamp}/'
            df.dropDuplicates(['id']) \
              .write.mode('overwrite') \
              .partitionBy('year', 'month') \
              .json(out_path)
        except Exception as e:
            raise RuntimeError(f"Error writing enriched data: {e}")

    def run(self, key, timestamp):
        """Execute full pipeline: normalize, derive, enrich, dedup, write."""
        input_path = f's3://{self.raw_bucket}/{key}'
        df = self.spark.read.json(input_path)
        df = self.normalize_casts(df)
        df = self.derive_fields(df)
        df = self.lookup_enrich(df)
        self.dedup_and_write(df, timestamp)
        self.spark.stop()
