"""
Unit tests for monitoring module.
"""

import json
import os
import unittest
from unittest.mock import patch, MagicMock


class TestMonitoring(unittest.TestCase):

    @patch("boto3.client")
    def test_monitor_glue_jobs_alerts_on_failure(self, mock_boto):
        """Test that a FAILED job run triggers an SNS publish."""
        mock_glue, mock_sns = MagicMock(), MagicMock()
        mock_boto.side_effect = lambda service, *a, **kw: {"glue": mock_glue, "sns": mock_sns}[service]
        mock_glue.get_job_runs.return_value = {
            "JobRuns": [{"Id": "run-1", "JobRunState": "FAILED", "ErrorMessage": "boom"}]
        }

        from monitoring.monitoring import monitor_glue_jobs
        failures = monitor_glue_jobs(job_names=["my-job"], sns_topic_arn="arn:aws:sns:us-east-1:123:topic")

        self.assertEqual(len(failures), 1)
        mock_sns.publish.assert_called_once()

    @patch("boto3.client")
    def test_monitor_glue_jobs_no_alert_when_healthy(self, mock_boto):
        """Test that no SNS publish happens when all job runs succeeded."""
        mock_glue, mock_sns = MagicMock(), MagicMock()
        mock_boto.side_effect = lambda service, *a, **kw: {"glue": mock_glue, "sns": mock_sns}[service]
        mock_glue.get_job_runs.return_value = {"JobRuns": [{"Id": "run-1", "JobRunState": "SUCCEEDED"}]}

        from monitoring.monitoring import monitor_glue_jobs
        failures = monitor_glue_jobs(job_names=["my-job"], sns_topic_arn="arn:aws:sns:us-east-1:123:topic")

        self.assertEqual(failures, [])
        mock_sns.publish.assert_not_called()

    @patch("boto3.client")
    def test_detect_schema_drift_alerts_when_fields_change(self, mock_boto):
        """Test that a changed field set triggers an SNS publish and updates the snapshot."""
        mock_s3, mock_sns = MagicMock(), MagicMock()
        mock_boto.side_effect = lambda service, *a, **kw: {"s3": mock_s3, "sns": mock_sns}[service]
        mock_s3.get_object.side_effect = [
            {"Body": MagicMock(read=lambda: json.dumps({"id": 1, "new_field": "x"}).encode())},
            {"Body": MagicMock(read=lambda: json.dumps(["id", "old_field"]).encode())},
        ]

        from monitoring.monitoring import detect_schema_drift
        drifted = detect_schema_drift("bucket", ["key1"], sns_topic_arn="arn:aws:sns:us-east-1:123:topic")

        self.assertTrue(drifted)
        mock_sns.publish.assert_called_once()
        mock_s3.put_object.assert_called_once()


if __name__ == "__main__":
    unittest.main()
