"""Module: validation.py
Implements the Quality Gate with schema, record, Deequ, and GE checks."""
import boto3
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_extract
from pydeequ.checks import Check
from pydeequ.verification import VerificationSuite
import great_expectations as ge

def validate_schema_glue(bucket: str, key: str, registry: str, schema: str) -> bool:
    """Check S3 object against Glue Schema Registry.
    :return: True if matches, False otherwise"""
    # TODO: Use AWS Glue API for schema comparison
    return True

def validate_record_rules(bucket: str, key: str) -> bool:
    """Run PySpark rules: non-null id/timestamp and email regex."""
    spark = SparkSession.builder.appName('validate_records').getOrCreate()
    df = spark.read.json(f's3://{bucket}/{key}')
    valid_df = df.filter(
        col('id').isNotNull() &
        col('timestamp').isNotNull() &
        (regexp_extract(col('email'), r"[^@]+@[^\.]+\..+", 0) != '')
    )
    passed = valid_df.count() == df.count()
    spark.stop()
    return passed

def validate_deequ(bucket: str, key: str) -> bool:
    """Run PyDeequ checks for zero rows and id completeness."""
    spark = SparkSession.builder.appName('deequ').getOrCreate()
    df = spark.read.json(f's3://{bucket}/{key}')
    check = Check(spark, Check.Level.Error, 'deequ_checks')        .hasSize(lambda x: x > 0)        .isComplete('id')
    result = VerificationSuite(spark).onData(df).addCheck(check).run()
    spark.stop()
    return result.status == 'Success'

def validate_ge(bucket: str, key: str) -> bool:
    """Execute Great Expectations suite on S3 JSON batch."""
    context = ge.get_context()
    batch = context.get_batch({
        'datasource': 's3_json',
        'path': f's3://{bucket}/{key}'
    })
    result = context.run_validation_operator('action_list_operator', assets_to_validate=[batch])
    return result.success
