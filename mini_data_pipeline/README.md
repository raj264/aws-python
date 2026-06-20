# 🚀 Mini Data Ingestion Pipeline on AWS

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

## 🌟 Overview

A serverless ingestion pipeline supporting multiple data sources:

- 🛰 FTP/SFTP
- 🌐 REST, SOAP, GraphQL, gRPC APIs
- 🔁 Kinesis Streams

Each record is validated (schema + record-level rules, PyDeequ, Great Expectations), transformed/enriched (PySpark), written to a curated Parquet zone, registered in the Glue Data Catalog with Lake Formation permissions, and monitored via CloudWatch/SNS with schema-drift detection.

## 🔧 Technologies Used

- **AWS Lambda** – Orchestration (`orchestration/handler.py`)
- **AWS S3** – Raw, staging, quarantine, enriched, curated zones
- **AWS Glue / Glue Data Catalog / Lake Formation** – Schema registry, cataloging, governance
- **PySpark, PyDeequ, Great Expectations** – Validation and transformation
- **CloudWatch, SNS** – Job monitoring, failure alerts, schema-drift alerts

## 📁 Project Structure

```
mini_data_pipeline/
├── ingestion/         # FTP, REST/SOAP/GraphQL/gRPC, Kinesis ingestion
├── processing/        # Schema/record validation, transformation, curated-zone writes
├── catalog/           # Glue crawler + Lake Formation permission grants
├── monitoring/        # Glue job failure alerts, schema-drift detection
├── orchestration/     # Lambda handler tying every stage together
├── config/            # Standalone settings module (not currently wired into orchestration/handler.py, which reads os.environ directly)
├── tests/             # pytest suite
├── main.py            # Local entry point - invokes orchestration.handler.lambda_handler
└── requirements.txt
```

## ⚙️ How to Run

1. **Set required environment variables** (see `.env.example` at the repo root):
   ```bash
   export RAW_BUCKET=... STAGING_PREFIX=... QUARANTINE_PREFIX=... ENRICHED_PREFIX=... CURATED_PREFIX=...
   export SNS_TOPIC_ARN=...
   # PyDeequ requires this at import time - must match an installed Spark version
   export SPARK_VERSION=3.5
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the pipeline locally**:
   ```bash
   python main.py
   ```

4. **Deploy** `orchestration/handler.py` as the Lambda entry point, with `layer/` containing the shared dependencies.

## 🧪 Running Tests

```bash
SPARK_VERSION=3.5 pytest tests/ -v
```

Tests mock boto3 (S3, Glue, SNS) and cover ingestion, schema validation, curated-zone registration, and monitoring/drift-detection logic.

## 📌 Example Athena Query

```sql
SELECT * FROM curated_db.curated_table LIMIT 10;
```

## 📣 Highlights

- Multi-protocol ingestion
- Schema + record-level + PyDeequ + Great Expectations quality gates
- Partitioned, queryable Parquet output registered in Glue/Athena
- Lake Formation-governed metadata access
- SNS alerting on Glue job failures and schema drift

## 📜 License

MIT License - see [LICENSE](../LICENSE).
