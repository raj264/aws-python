"""Module: kinesis_ingest.py
Lambda handler to ingest real-time data from Kinesis into the raw S3 zone."""
import boto3
import os
import base64
import time

def handler(event, context):
    """Process Kinesis stream records and upload each to S3.
    :param event: AWS Lambda event payload
    :param context: Lambda context
    :return: Processing summary
    """
    s3 = boto3.client('s3')
    bucket = os.environ['RAW_BUCKET']
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data'])
        date_prefix = time.strftime('%Y/%m/%d')
        key = f"kinesis/{date_prefix}/{record['kinesis']['sequenceNumber']}.json"
        s3.put_object(Bucket=bucket, Key=key, Body=payload)
    return {'status': 'processed', 'count': len(event['Records'])}
