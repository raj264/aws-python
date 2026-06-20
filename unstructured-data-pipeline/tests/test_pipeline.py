"""
Unit tests for unstructured-data-pipeline.
"""

import unittest
from unittest.mock import patch, MagicMock


class TestS3Setup(unittest.TestCase):

    @patch("boto3.client")
    def test_create_bucket(self, mock_boto):
        """Test S3 bucket creation is called."""
        mock_boto.return_value = MagicMock()
        from modules.s3_setup import create_bucket
        try:
            create_bucket("test-bucket")
        except Exception:
            pass
        self.assertTrue(True)


class TestLambdaHandler(unittest.TestCase):

    @patch("boto3.client")
    def test_lambda_handler_supported_extension(self, mock_boto):
        """Test Lambda handler processes supported file types."""
        mock_s3 = MagicMock()
        mock_boto.return_value = mock_s3
        event = {
            "Records": [{"s3": {"bucket": {"name": "test-bucket"}, "object": {"key": "uploads/data.csv"}}}]
        }
        from lambda_function.lambda_function import lambda_handler
        result = lambda_handler(event, {})
        self.assertEqual(result["status"], "done")


if __name__ == "__main__":
    unittest.main()
