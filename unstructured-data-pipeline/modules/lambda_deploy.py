import boto3
import zipfile
import os
from botocore.exceptions import ClientError

# AWS configuration
AWS_REGION = 'us-east-1'
lambda_client = boto3.client('lambda', region_name=AWS_REGION)

def deploy_lambda_function(role_arn="arn:aws:iam::123456789012:role/LambdaExecutionRole"):
    """
    Deploys an AWS Lambda function that listens for S3 events and moves
    supported files (.csv, .json, .xml, .txt) to a staging folder.

    Parameters:
    - role_arn (str): The ARN of the IAM role with Lambda execution permissions.
                      Default should be replaced with your actual IAM role ARN.
    """

    # Load Lambda handler code from external Python file
    lambda_code_path = 'lambda_function/lambda_function.py'
    with open(lambda_code_path, 'r') as f:
        lambda_code = f.read()

    # Create a temporary directory to build the deployment package
    build_dir = 'lambda_build'
    os.makedirs(build_dir, exist_ok=True)

    lambda_source_file = os.path.join(build_dir, 'lambda_function.py')
    with open(lambda_source_file, 'w') as f:
        f.write(lambda_code)

    # Create ZIP package for Lambda deployment
    zip_file_path = os.path.join(build_dir, 'deployment_package.zip')
    with zipfile.ZipFile(zip_file_path, 'w') as z:
        z.write(lambda_source_file, arcname='lambda_function.py')

    # Load zipped code
    with open(zip_file_path, 'rb') as f:
        zipped_code = f.read()

    try:
        # Deploy the Lambda function
        lambda_client.create_function(
            FunctionName='UnstructuredDataLambda',
            Runtime='python3.9',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zipped_code},
            Timeout=60,
            MemorySize=128,
        )
        print("[Lambda] Function 'UnstructuredDataLambda' created successfully.")
    except ClientError as e:
        print("[Lambda] Error creating function:", e)
