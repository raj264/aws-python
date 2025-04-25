from modules.s3_setup import create_bucket
from modules.lambda_deploy import deploy_lambda_function
from modules.glue_setup import setup_glue_resources

# Default AWS resource names
RAW_BUCKET = 'unstructured-raw-data-bucket'
PROCESSED_BUCKET = 'unstructured-processed-data-bucket'

# Replace these with your actual IAM Role ARNs
DEFAULT_LAMBDA_ROLE_ARN = "arn:aws:iam::123456789012:role/MyLambdaExecutionRole"
DEFAULT_GLUE_ROLE_ARN = "arn:aws:iam::123456789012:role/MyGlueCrawlerRole"

def main(lambda_role_arn=DEFAULT_LAMBDA_ROLE_ARN, glue_role_arn=DEFAULT_GLUE_ROLE_ARN):
    """
    Main function to orchestrate the setup of the unstructured data pipeline.
    This includes:
      - Creating raw and processed S3 buckets
      - Deploying a Lambda function to monitor and move files
      - Creating Glue resources to catalog data
    Parameters:
      - lambda_role_arn (str): IAM Role ARN for the Lambda function
      - glue_role_arn (str): IAM Role ARN for the Glue crawler
    """
    print("\n--- Starting AWS Unstructured Data Pipeline Setup ---\n")

    # Step 1: Create S3 buckets
    create_bucket(RAW_BUCKET)
    create_bucket(PROCESSED_BUCKET)

    # Step 2: Deploy Lambda function
    deploy_lambda_function(role_arn=lambda_role_arn)

    # Step 3: Set up AWS Glue crawler and catalog
    setup_glue_resources(role_arn=glue_role_arn)

    print("\n--- Setup Complete. You're ready to upload unstructured files to the raw bucket. ---")

if __name__ == '__main__':
    main()
