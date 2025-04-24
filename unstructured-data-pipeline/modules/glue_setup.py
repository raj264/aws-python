import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'us-east-1'
RAW_BUCKET = 'unstructured-raw-data-bucket'
glue = boto3.client('glue', region_name=AWS_REGION)

def setup_glue_resources():
    """
    Set up AWS Glue database and crawler to catalog unstructured files in S3.
    """
    role_arn = input("Enter your Glue IAM role ARN: ")

    try:
        glue.create_database(Name='unstructured_data_db')
        print("[Glue] Database created.")
    except:
        print("[Glue] Database may already exist.")

    try:
        glue.create_crawler(
            Name='unstructured_crawler',
            Role=role_arn,
            DatabaseName='unstructured_data_db',
            Targets={'S3Targets': [{'Path': f's3://{RAW_BUCKET}/staging/'}]},
            TablePrefix='unstructured_'
        )
        print("[Glue] Crawler created.")
    except ClientError as e:
        print("[Glue] Error creating crawler:", e)