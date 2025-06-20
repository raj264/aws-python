"""Module: handler.py
AWS Lambda orchestrator for ingest → validate → route → transform → curated."""
import os
import json
import time
import boto3
from ftp_ingest import download_from_ftp, upload_to_s3
from api_ingest import fetch_rest_api_data, fetch_soap_api_data, fetch_graphql_data, fetch_grpc_data, upload_json_to_s3
from validation import validate_schema_glue, validate_record_rules, validate_deequ, validate_ge
from transformation import TransformationJob
from curated_zone import write_curated_parquet, register_athena_table
from metadata_catalog import run_glue_crawler, grant_lakeformation_permissions
from monitoring import monitor_glue_jobs, detect_schema_drift

# Initialize AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Environment variables
RAW_BUCKET = os.environ['RAW_BUCKET']
STAGING_PREFIX = os.environ['STAGING_PREFIX']
QUARANTINE_PREFIX = os.environ['QUARANTINE_PREFIX']
ENRICHED_PREFIX = os.environ['ENRICHED_PREFIX']
CURATED_PREFIX = os.environ['CURATED_PREFIX']
SNS_TOPIC = os.environ['SNS_TOPIC_ARN']

# Transformation and metadata config
LOOKUP_JDBC_URL = os.environ.get('LOOKUP_JDBC_URL')
LOOKUP_TABLE = os.environ.get('LOOKUP_TABLE')
GLUE_CRAWLER_NAME = os.environ.get('GLUE_CRAWLER_NAME')

def lambda_handler(event, context):
    """Main pipeline orchestration entrypoint."""
    timestamp = time.strftime('%Y/%m/%d/%H%M%S')
    ingested = []

    # Ingest from REST, SOAP, GraphQL (gRPC omitted)
    rest = fetch_rest_api_data(os.environ['REST_URL'], headers={'Authorization': f"Bearer {os.environ['REST_TOKEN']}"})
    key_rest = f"api/rest/{timestamp}.json"; upload_json_to_s3(rest, RAW_BUCKET, key_rest); ingested.append(key_rest)
    soap = fetch_soap_api_data(os.environ['SOAP_WSDL'], os.environ['SOAP_METHOD'], **json.loads(os.environ.get('SOAP_PARAMS','{}')))
    key_soap = f"api/soap/{timestamp}.json"; upload_json_to_s3(soap, RAW_BUCKET, key_soap); ingested.append(key_soap)
    gql = fetch_graphql_data(os.environ['GRAPHQL_ENDPOINT'], os.environ['GRAPHQL_QUERY'], headers={'Authorization': f"Bearer {os.environ['GRAPHQL_TOKEN']}"})
    key_gql = f"api/graphql/{timestamp}.json"; upload_json_to_s3(gql, RAW_BUCKET, key_gql); ingested.append(key_gql)

    results = {'passed':[], 'failed':[]}
    # Validate each file
    for key in ingested:
        if not validate_schema_glue(RAW_BUCKET, key, os.environ['SCHEMA_REGISTRY'], os.environ['SCHEMA_NAME']):
            results['failed'].append(key); continue
        if not validate_record_rules(RAW_BUCKET, key):
            results['failed'].append(key); continue
        if not validate_deequ(RAW_BUCKET, key):
            results['failed'].append(key); continue
        if not validate_ge(RAW_BUCKET, key):
            results['failed'].append(key); continue
        results['passed'].append(key)

    def route(src, prefix):
        dest = prefix + src
        s3.copy_object(Bucket=RAW_BUCKET, CopySource={'Bucket':RAW_BUCKET,'Key':src}, Key=dest)
        s3.delete_object(Bucket=RAW_BUCKET, Key=src)
        return dest

    # Route passes and failures
    for k in results['passed']: route(k, STAGING_PREFIX)
    for k in results['failed']:
        new_k = route(k, QUARANTINE_PREFIX)
        sns.publish(TopicArn=SNS_TOPIC, Subject='Data Quarantine', Message=f"{new_k} failed validations")

    # Transform staged
    transformer = TransformationJob(RAW_BUCKET, STAGING_PREFIX, ENRICHED_PREFIX, LOOKUP_JDBC_URL, LOOKUP_TABLE)
    for k in results['passed']:
        rel = k.replace(STAGING_PREFIX, '')
        transformer.run(rel, timestamp)

    # Curate enriched to Parquet and register
    for k in results['passed']:
        enriched_key = ENRICHED_PREFIX + k.replace(STAGING_PREFIX, '')
        parquet_path = write_curated_parquet(RAW_BUCKET, enriched_key, CURATED_PREFIX, timestamp)
        register_athena_table(RAW_BUCKET, parquet_path)

    # Update metadata and run crawler
    run_glue_crawler(GLUE_CRAWLER_NAME)

    # Monitoring checks
    monitor_glue_jobs()
    detect_schema_drift(RAW_BUCKET, results['passed'])

    return {'status':'done','results':results}
