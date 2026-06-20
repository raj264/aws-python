# Unstructured Data Pipeline on AWS

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![AWS](https://img.shields.io/badge/AWS-Serverless-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A serverless pipeline on AWS to ingest, stage, and catalog unstructured data (CSV, JSON, XML, TXT) using Lambda, Glue, and S3, enabling downstream querying via Athena and dashboarding via QuickSight.

## ✅ Supported File Types

CSV, JSON, XML, TXT

## 🎯 Purpose

Automate ingestion of unstructured data formats into a structured, queryable form without manual ETL work.

## ⚙️ Architecture

1. **S3** – Input files uploaded to a source bucket.
2. **Lambda** (`lambda_function/lambda_function.py`) – Triggered by upload, moves supported file types into a `staging/` prefix.
3. **Glue Crawler** – Catalogs staged data into the Glue Data Catalog.
4. **Glue Job** – Transforms data into Parquet and loads it to a target S3 location.
5. **Amazon Athena** – SQL querying over cataloged data.
6. **Amazon QuickSight** – Dashboards on top of Athena.

## 📁 Project Structure

```
unstructured-data-pipeline/
├── data_pipeline.py             # Orchestrates bucket/Lambda/Glue setup
├── requirements.txt
├── modules/
│   ├── s3_setup.py              # Raw/processed bucket creation
│   ├── lambda_deploy.py         # Packages and deploys the staging Lambda
│   └── glue_setup.py            # Glue database + crawler creation
├── lambda_function/
│   └── lambda_function.py       # Lambda handler: routes supported files to staging/
└── tests/
    └── test_pipeline.py
```

## 🚀 Getting Started

```bash
pip install -r requirements.txt

# Required - no fallback default, must point at real IAM roles in your account
export LAMBDA_ROLE_ARN=arn:aws:iam::<ACCOUNT_ID>:role/LambdaExecutionRole
export GLUE_ROLE_ARN=arn:aws:iam::<ACCOUNT_ID>:role/GlueCrawlerRole

python data_pipeline.py
```

## 🧪 Running Tests

```bash
pytest tests/ -v
```

## 🧭 Example Flow

1. Upload `sample.csv` to the raw bucket.
2. Lambda copies it to `staging/`.
3. Glue Crawler catalogs it.
4. Glue Job transforms it to Parquet in the processed bucket.
5. Query it in Athena; visualize in QuickSight.

## 🔧 Requirements

- Python 3.9+
- AWS credentials configured (`~/.aws/credentials`)
- IAM role with permissions for S3, Lambda, Glue, Athena, and QuickSight

## 📌 Notes

- Add support for more formats by extending `lambda_function.py`'s `supported_ext` list.
- Extend for streaming sources using Amazon Kinesis.
