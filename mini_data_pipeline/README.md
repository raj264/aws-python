# 🚀 Mini Data Ingestion Pipeline on AWS

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Status](https://img.shields.io/badge/status-production-green)]()

---

## 🌟 Overview

This project demonstrates a complete serverless data pipeline on AWS supporting multiple data sources including:

- 🛰 FTP/SFTP
- 🌐 REST, SOAP, GraphQL, gRPC APIs
- 🔁 Kinesis Streams

Each stage is modularized, validated, enriched, and stored securely using AWS services like Glue, S3, Lake Formation, and monitored via CloudWatch.

---

## 🔧 Technologies Used

- **AWS Glue / EMR** – Validation, transformation
- **AWS Lambda** – Orchestration
- **AWS S3** – Raw, staging, curated zones
- **Glue Data Catalog & Lake Formation** – Metadata management
- **PySpark, PyDeequ, Great Expectations** – Quality & processing
- **CloudWatch, SNS** – Monitoring & alerting

---

## 📁 Project Structure

```
mini_data_pipeline/
│
├── ingestion/         # FTP, API, Kinesis ingestion
├── processing/        # Validation, transformation, writing curated data
├── catalog/           # Metadata registration (Glue, Lake Formation)
├── monitoring/        # Alerting & drift detection
├── orchestration/     # Lambda handlers
├── config/            # Environment config
├── main.py            # Central orchestrator
├── requirements.txt
├── README.md
```

---

## ⚙️ How to Run

1. **Set environment variables**:
   ```bash
   export RAW_BUCKET=...
   export REST_URL=...
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the pipeline**:
   ```bash
   python main.py
   ```

4. **Deploy to AWS** using Lambda, Glue, and CloudFormation/CDK.

---

## 📊 Architecture Diagram

> *(Insert your architecture diagram here — optionally export from Lucidchart or draw.io)*

---

## 📌 Example Athena Query

```sql
SELECT * FROM curated_db.curated_table LIMIT 10;
```

---

## 📣 Highlights

✅ Multi-protocol ingestion  
✅ Robust data quality gates  
✅ Partitioned, queryable Parquet outputs  
✅ Secure and governed metadata access  
✅ Alerting for schema drifts and failures

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Connect

Feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/raj264) or ⭐ the repository if you find it helpful!

