"""
Main entry point for the Mini Data Ingestion Pipeline.
This script orchestrates the data flow from ingestion to monitoring.
"""

import logging

# Importing modules from respective packages
from ingestion.ftp_ingest import ingest_from_ftp
from ingestion.api_ingest import ingest_from_api
from ingestion.kinesis_ingest import ingest_from_kinesis

from processing.validation import validate_data
from processing.transformation import transform_data
from processing.curated_zone import write_to_curated_zone

from catalog.metadata_catalog import register_metadata
from monitoring.monitoring import monitor_pipeline


def run_pipeline():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting data ingestion phase...")
        ingest_from_ftp()
        ingest_from_api()
        ingest_from_kinesis()
    except Exception as e:
        logger.exception("Error during ingestion: %s", e)

    try:
        logger.info("Running validation...")
        validate_data()
    except Exception as e:
        logger.exception("Error during validation: %s", e)

    try:
        logger.info("Applying transformation...")
        transform_data()
    except Exception as e:
        logger.exception("Error during transformation: %s", e)

    try:
        logger.info("Writing to curated zone...")
        write_to_curated_zone()
    except Exception as e:
        logger.exception("Error during curated zone write: %s", e)

    try:
        logger.info("Registering metadata...")
        register_metadata()
    except Exception as e:
        logger.exception("Error during metadata registration: %s", e)

    try:
        logger.info("Monitoring pipeline...")
        monitor_pipeline()
    except Exception as e:
        logger.exception("Error during monitoring: %s", e)

    logger.info("Pipeline completed.")


if __name__ == "__main__":
    run_pipeline()
