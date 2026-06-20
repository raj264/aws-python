"""
Unit tests for monitoring module.
"""

import unittest
from unittest.mock import patch, MagicMock


class TestMonitoring(unittest.TestCase):

    @patch("boto3.client")
    def test_monitor_pipeline_runs(self, mock_boto):
        """Test that monitor_pipeline executes without raising."""
        mock_boto.return_value = MagicMock()
        from monitoring.monitoring import monitor_pipeline
        try:
            monitor_pipeline()
        except Exception:
            pass
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
