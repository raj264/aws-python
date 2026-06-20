"""
Main entry point for the Mini Data Ingestion Pipeline.
Locally invokes the same orchestration logic used by the Lambda handler
(orchestration/handler.py), so there is a single source of truth for the
ingest -> validate -> route -> transform -> curated flow.
"""

import logging

from orchestration.handler import lambda_handler


def run_pipeline():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Starting pipeline run...")
    try:
        result = lambda_handler({}, None)
        logger.info("Pipeline completed: %s", result)
        return result
    except Exception:
        logger.exception("Pipeline run failed")
        raise


if __name__ == "__main__":
    run_pipeline()
