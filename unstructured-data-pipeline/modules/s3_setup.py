import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'us-east-1'
s3 = boto3.client('s3', region_name=AWS_REGION)

def create_bucket(bucket_name):
    """
    Create an Amazon S3 bucket in the specified region if it does not exist.

    Parameters:
        bucket_name (str): The name of the bucket to create.
    """
    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': AWS_REGION})
        print(f"[S3] Bucket '{bucket_name}' created.")
    except ClientError as e:
        print(f"[S3] Error or bucket already exists: {e}")