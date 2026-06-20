"""Module: monitoring.py
Implements CloudWatch monitoring, SNS alerts, and schema drift detection."""
import os

import boto3
import json
from botocore.exceptions import ClientError

def monitor_glue_jobs(job_names: list = None, sns_topic_arn: str = None):
    """Check recent Glue job run statuses and publish an SNS alert for any FAILED runs."""
    glue = boto3.client('glue')
    sns = boto3.client('sns')
    sns_topic_arn = sns_topic_arn or os.environ['SNS_TOPIC_ARN']
    job_names = job_names or [job['Name'] for job in glue.get_jobs()['Jobs']]

    failures = []
    for job_name in job_names:
        runs = glue.get_job_runs(JobName=job_name, MaxResults=5)['JobRuns']
        failures.extend(
            f"{job_name} run {run['Id']}: {run.get('ErrorMessage', 'unknown error')}"
            for run in runs if run['JobRunState'] == 'FAILED'
        )

    if failures:
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject='Glue Job Failures Detected',
            Message='\n'.join(failures),
        )
    return failures

def detect_schema_drift(bucket: str, keys: list, sns_topic_arn: str = None,
                         schema_snapshot_key: str = 'schema/last_schema.json'):
    """Compare the field set of newly ingested records against the last known
    schema snapshot stored in S3; alert via SNS and update the snapshot if changed."""
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    sns_topic_arn = sns_topic_arn or os.environ['SNS_TOPIC_ARN']

    current_fields = set()
    for key in keys:
        obj = s3.get_object(Bucket=bucket, Key=key)
        record = json.loads(obj['Body'].read())
        current_fields.update(record.keys())

    try:
        snapshot_obj = s3.get_object(Bucket=bucket, Key=schema_snapshot_key)
        previous_fields = set(json.loads(snapshot_obj['Body'].read()))
    except ClientError:
        previous_fields = set()

    drifted = current_fields != previous_fields
    if drifted and previous_fields:
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject='Schema Drift Detected',
            Message=(
                f"Added fields: {sorted(current_fields - previous_fields)}\n"
                f"Removed fields: {sorted(previous_fields - current_fields)}"
            ),
        )

    s3.put_object(
        Bucket=bucket,
        Key=schema_snapshot_key,
        Body=json.dumps(sorted(current_fields)),
    )
    return drifted
