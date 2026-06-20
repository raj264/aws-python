"""
Unit tests for ingestion modules.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open


class TestFTPIngest(unittest.TestCase):

    @patch("ftplib.FTP")
    def test_download_from_ftp_connects_and_retrieves(self, mock_ftp_class):
        """Test that FTP connection/login/retrieval happen with the right arguments."""
        mock_ftp = MagicMock()
        mock_ftp_class.return_value = mock_ftp
        from ingestion.ftp_ingest import download_from_ftp

        with patch("builtins.open", mock_open()):
            download_from_ftp("ftp.example.com", 21, "user", "pass", "/remote/file.csv", "/tmp/file.csv")

        mock_ftp.connect.assert_called_once_with("ftp.example.com", 21)
        mock_ftp.login.assert_called_once_with("user", "pass")
        mock_ftp.retrbinary.assert_called_once()
        mock_ftp.quit.assert_called_once()


class TestAPIIngest(unittest.TestCase):

    @patch("requests.get")
    def test_fetch_rest_api_data_returns_json(self, mock_get):
        """Test that REST ingestion makes an HTTP GET request and returns parsed JSON."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response

        from ingestion.api_ingest import fetch_rest_api_data
        result = fetch_rest_api_data("https://api.example.com/data")

        mock_get.assert_called_once_with("https://api.example.com/data", headers=None, params=None)
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(result, {"data": []})


class TestKinesisIngest(unittest.TestCase):

    @patch("boto3.client")
    def test_handler_uploads_each_record_to_s3(self, mock_boto):
        """Test that the Kinesis Lambda handler uploads each record to S3."""
        mock_s3 = MagicMock()
        mock_boto.return_value = mock_s3

        from ingestion.kinesis_ingest import handler
        import base64
        import os

        os.environ["RAW_BUCKET"] = "test-bucket"
        event = {
            "Records": [
                {"kinesis": {"data": base64.b64encode(b'{"id": 1}').decode(), "sequenceNumber": "1"}},
                {"kinesis": {"data": base64.b64encode(b'{"id": 2}').decode(), "sequenceNumber": "2"}},
            ]
        }
        result = handler(event, None)

        self.assertEqual(mock_s3.put_object.call_count, 2)
        self.assertEqual(result, {"status": "processed", "count": 2})


if __name__ == "__main__":
    unittest.main()
