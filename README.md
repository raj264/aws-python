# 🧠 AWS + Python Projects

Welcome to **aws-python** — a curated collection of serverless data projects built using **AWS services** and **Python**. Each mini-project is modular, cloud-native, and designed to be reusable in real-world scenarios.

---

## 📦 Projects

### 🔹 [Unstructured Data Pipeline](./unstructured-data-pipeline/README.md)
A fully automated pipeline for ingesting and transforming unstructured data files (CSV, JSON, XML, TXT) using:
- **Amazon S3** for storage
- **AWS Lambda** for event-driven staging
- **AWS Glue** for cataloging and preparing the data

> 💡 Easily adaptable to any unstructured format. Great for data lake ingestion.

---

## 🔧 Technologies Used

- Python 3.9+
- AWS SDK for Python (`boto3`)
- AWS services: S3, Lambda, Glue, IAM

---

## 📁 Structure

aws-python/
├── README.md
└── unstructured-data-pipeline/
    ├── README.md
    ├── data_pipeline.py
    ├── requirements.txt
    ├── lambda_function/
    │   └── lambda_function.py
    └── modules/
        ├── glue_setup.py
        ├── lambda_deploy.py
        └── s3_setup.py

---

## 🚀 How to Use This Repo

```bash
# Clone the repo
git clone https://github.com/raj264/aws-python.git
cd aws-python

# Go into a project and follow its README
cd unstructured-data-pipeline
pip install -r requirements.txt
python data_pipeline.py
