from modules.s3_setup import create_bucket
from modules.lambda_deploy import deploy_lambda_function
from modules.glue_setup import setup_glue_resources

RAW_BUCKET = 'unstructured-raw-data-bucket'
PROCESSED_BUCKET = 'unstructured-processed-data-bucket'

def main():
    """
    Main entry point for initializing the unstructured data pipeline.
    It creates required S3 buckets, deploys the Lambda function,
    and sets up the Glue catalog and crawler for later ETL processes.
    """
    print("\n--- Starting AWS Unstructured Data Pipeline Setup ---\n")
    create_bucket(RAW_BUCKET)
    create_bucket(PROCESSED_BUCKET)
    deploy_lambda_function()
    setup_glue_resources()
    print("\n--- Setup Complete. You can now upload supported file types to the raw bucket. ---")

if __name__ == '__main__':
    main()