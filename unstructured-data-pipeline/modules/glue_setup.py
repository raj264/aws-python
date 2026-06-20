import os

import boto3
from botocore.exceptions import ClientError

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
RAW_BUCKET = os.getenv('RAW_BUCKET', 'unstructured-raw-data-bucket')

# Initialize Glue client
glue = boto3.client('glue', region_name=AWS_REGION)

def setup_glue_resources(role_arn=None):
    """
    Creates a Glue database and a crawler to catalog unstructured data files
    stored in the 'staging' folder of the raw data S3 bucket.

    Parameters:
    - role_arn (str): The ARN of the IAM role with Glue permissions.
                      Falls back to the GLUE_ROLE_ARN environment variable.
    """
    role_arn = role_arn or os.environ['GLUE_ROLE_ARN']

    database_name = "unstructured_data_db"
    crawler_name = "unstructured_crawler"

    try:
        glue.create_database(Name=database_name)
        print(f"[Glue] Database '{database_name}' created.")
    except ClientError as e:
        if 'AlreadyExistsException' in str(e):
            print(f"[Glue] Database '{database_name}' already exists.")
        else:
            print("[Glue] Error creating database:", e)

    try:
        glue.create_crawler(
            Name=crawler_name,
            Role=role_arn,
            DatabaseName=database_name,
            Targets={'S3Targets': [{'Path': f's3://{RAW_BUCKET}/staging/'}]},
            TablePrefix='unstructured_',
            SchemaChangePolicy={
                'UpdateBehavior': 'UPDATE_IN_DATABASE',
                'DeleteBehavior': 'LOG'
            }
        )
        print(f"[Glue] Crawler '{crawler_name}' created.")
    except ClientError as e:
        if 'AlreadyExistsException' in str(e):
            print(f"[Glue] Crawler '{crawler_name}' already exists.")
        else:
            print("[Glue] Error creating crawler:", e)
