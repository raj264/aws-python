# 🧠 AWS + Python Projects

A curated collection of serverless data projects built using **AWS services** and **Python**. Each mini-project is modular, cloud-native, and designed to be reusable in real-world scenarios.

---

## 📦 Projects

### 🔹 [Unstructured Data Pipeline](./unstructured-data-pipeline/README.md)
Ingests unstructured files (CSV, JSON, XML, TXT) from S3, stages them via a Lambda trigger, and catalogs them with Glue for querying via Athena/QuickSight.

### 🔹 [Mini Data Pipeline](./mini_data_pipeline/README.md)
A multi-protocol ingestion pipeline (FTP/SFTP, REST/SOAP/GraphQL/gRPC, Kinesis) with a PySpark/PyDeequ/Great Expectations quality gate, Glue Data Catalog + Lake Formation metadata management, and CloudWatch/SNS monitoring with schema-drift detection.

---

## 🔧 Technologies Used

- Python 3.9+
- AWS SDK for Python (`boto3`)
- AWS services: S3, Lambda, Glue, Kinesis, Redshift, Lake Formation, CloudWatch, SNS, IAM

---

## 📁 Structure

```
aws-python/
├── README.md
├── unstructured-data-pipeline/   # S3 -> Lambda -> Glue -> Athena
└── mini_data_pipeline/           # Multi-protocol ingestion -> quality gate -> curated zone
```

Each sub-project has its own README with setup, environment variables, and testing instructions.

---

## 🚀 How to Use This Repo

```bash
git clone https://github.com/raj264/aws-python.git
cd aws-python

# Go into a project and follow its README
cd unstructured-data-pipeline   # or mini_data_pipeline
pip install -r requirements.txt
```
