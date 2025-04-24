import boto3
import zipfile
import os
from botocore.exceptions import ClientError

AWS_REGION = 'us-east-1'
lambda_client = boto3.client('lambda', region_name=AWS_REGION)

def deploy_lambda_function():
    """
    Deploys a Lambda function that processes files uploaded to S3.
    It checks for supported formats and moves them into a staging area.
    """
    role_arn = input("Enter your Lambda IAM role ARN: ")

    lambda_code = '''import boto3
import urllib.parse

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    supported_ext = ['.csv', '.json', '.xml', '.txt']
    for record in event['Records']:
        src_bucket = record['s3']['bucket']['name']
        src_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        if any(src_key.endswith(ext) for ext in supported_ext):
            dest_key = f'staging/{src_key.split("/")[-1]}'
            s3.copy_object(Bucket=src_bucket, CopySource={'Bucket': src_bucket, 'Key': src_key}, Key=dest_key)
            s3.delete_object(Bucket=src_bucket, Key=src_key)
    return {'status': 'done'}
'''

    os.makedirs('lambda_build', exist_ok=True)
    with open('lambda_build/lambda_function.py', 'w') as f:
        f.write(lambda_code)
    with zipfile.ZipFile('lambda_build/deployment_package.zip', 'w') as z:
        z.write('lambda_build/lambda_function.py', arcname='lambda_function.py')

    with open('lambda_build/deployment_package.zip', 'rb') as f:
        zipped_code = f.read()

    try:
        lambda_client.create_function(
            FunctionName='UnstructuredDataLambda',
            Runtime='python3.9',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zipped_code},
            Timeout=60,
            MemorySize=128,
        )
        print("[Lambda] Function 'UnstructuredDataLambda' created.")
    except ClientError as e:
        print("[Lambda] Error creating function:", e)