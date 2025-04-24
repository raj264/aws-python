# Unstructured Data Pipeline on AWS

This project sets up a fully automated, serverless pipeline on AWS to ingest, store, and catalog unstructured data (CSV, JSON, XML, TXT, etc.) using AWS Lambda, Glue, and S3. This enables downstream analytics using services like Amazon QuickSight.

## ✅ Supported File Types

- CSV
- JSON
- XML
- TXT

## 🧩 Features

- Upload unstructured files to an S3 bucket
- Automatically trigger a Lambda function to organize and validate files
- Catalog the data using AWS Glue for analysis
- Processed data stored separately for easy querying and reporting

## 🔧 AWS Services Used

- **Amazon S3** — Storage for raw and processed data
- **AWS Lambda** — Event-driven file mover and preprocessor
- **AWS Glue** — Catalog unstructured data and prepare for analytics
- **IAM** — Secure roles for Lambda and Glue
- **Amazon QuickSight** (optional) — Visualization

## 📁 Project Structure

```
unstructured-data-pipeline/
├── data_pipeline.py           # Main orchestration script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── modules/                   # Modular components
    ├── __init__.py
    ├── s3_setup.py            # S3 bucket setup
    ├── lambda_deploy.py       # Lambda function deployment
    └── glue_setup.py          # Glue crawler and catalog setup
```

## 🚀 Quick Start

### 🔹 Prerequisites

- Python 3.7+
- AWS credentials configured (via `aws configure` or IAM role)
- IAM Roles for Lambda and Glue created in advance

### 🔹 Setup

```bash
git clone https://github.com/yourusername/unstructured-data-pipeline.git
cd unstructured-data-pipeline
pip install -r requirements.txt
python data_pipeline.py
```

### 🔹 During Setup

You’ll be prompted to enter:
- Lambda IAM Role ARN
- Glue IAM Role ARN

These are used to allow the services to access S3 and other AWS resources securely.

## 📊 Visualization

Once data is cataloged by AWS Glue, you can connect Amazon QuickSight to:
```
s3://unstructured-processed-data-bucket/final/
```
And begin visualizing structured views of your formerly unstructured data.

## 🧾 License

MIT License