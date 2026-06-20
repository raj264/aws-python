"""
Centralized configuration for mini_data_pipeline.
All values are read from environment variables with sensible defaults.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# S3 Buckets
RAW_BUCKET = os.getenv("RAW_BUCKET", "mini-pipeline-raw")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", "mini-pipeline-staging")
CURATED_BUCKET = os.getenv("CURATED_BUCKET", "mini-pipeline-curated")

# IAM Role ARNs
LAMBDA_ROLE_ARN = os.getenv("LAMBDA_ROLE_ARN", "")
GLUE_ROLE_ARN = os.getenv("GLUE_ROLE_ARN", "")

# API
REST_URL = os.getenv("REST_URL", "")
API_KEY = os.getenv("API_KEY", "")

# Kinesis
KINESIS_STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "")

# FTP
FTP_HOST = os.getenv("FTP_HOST", "")
FTP_USER = os.getenv("FTP_USER", "")
FTP_PASSWORD = os.getenv("FTP_PASSWORD", "")
FTP_PATH = os.getenv("FTP_PATH", "/")

# SNS
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "")

# Glue
GLUE_DATABASE = os.getenv("GLUE_DATABASE", "mini_pipeline_db")
GLUE_CRAWLER = os.getenv("GLUE_CRAWLER", "mini_pipeline_crawler")
