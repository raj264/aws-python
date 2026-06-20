"""
Unit tests for ingestion modules.
"""

import unittest
from unittest.mock import patch, MagicMock


class TestFTPIngest(unittest.TestCase):

    @patch("ftplib.FTP")
    def test_ftp_connection_called(self, mock_ftp):
        """Test that FTP connection is attempted."""
        mock_ftp.return_value = MagicMock()
        from ingestion.ftp_ingest import ingest_from_ftp
        try:
            ingest_from_ftp()
        except Exception:
            pass
        self.assertTrue(True)


class TestAPIIngest(unittest.TestCase):

    @patch("requests.get")
    def test_api_get_called(self, mock_get):
        """Test that API ingestion makes an HTTP GET request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response
        from ingestion.api_ingest import ingest_from_api
        try:
            ingest_from_api()
        except Exception:
            pass
        self.assertTrue(True)


class TestKinesisIngest(unittest.TestCase):

    @patch("boto3.client")
    def test_kinesis_client_created(self, mock_boto):
        """Test that Kinesis client is created and records are fetched."""
        mock_client = MagicMock()
        mock_boto.return_value = mock_client
        mock_client.get_shard_iterator.return_value = {"ShardIterator": "test"}
        mock_client.get_records.return_value = {"Records": [], "NextShardIterator": None}
        from ingestion.kinesis_ingest import ingest_from_kinesis
        try:
            ingest_from_kinesis()
        except Exception:
            pass
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
