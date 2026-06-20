"""
Unit tests for processing modules.
"""

import json
import unittest
from unittest.mock import patch, MagicMock


class TestValidation(unittest.TestCase):

    @patch("boto3.client")
    def test_validate_schema_glue_accepts_matching_fields(self, mock_boto):
        """Test that a record whose fields are registered in the schema passes."""
        mock_glue, mock_s3 = MagicMock(), MagicMock()
        mock_boto.side_effect = lambda service, *a, **kw: {"glue": mock_glue, "s3": mock_s3}[service]
        mock_glue.get_schema_version.return_value = {
            "SchemaDefinition": json.dumps({"fields": [{"name": "id"}, {"name": "email"}]})
        }
        mock_s3.get_object.return_value = {"Body": MagicMock(read=lambda: json.dumps({"id": 1, "email": "a@b.com"}).encode())}

        from processing.validation import validate_schema_glue
        result = validate_schema_glue("bucket", "key.json", "registry", "schema")

        self.assertTrue(result)

    @patch("boto3.client")
    def test_validate_schema_glue_rejects_unregistered_fields(self, mock_boto):
        """Test that a record with fields not in the registered schema fails."""
        mock_glue, mock_s3 = MagicMock(), MagicMock()
        mock_boto.side_effect = lambda service, *a, **kw: {"glue": mock_glue, "s3": mock_s3}[service]
        mock_glue.get_schema_version.return_value = {
            "SchemaDefinition": json.dumps({"fields": [{"name": "id"}]})
        }
        mock_s3.get_object.return_value = {"Body": MagicMock(read=lambda: json.dumps({"id": 1, "unexpected": "x"}).encode())}

        from processing.validation import validate_schema_glue
        result = validate_schema_glue("bucket", "key.json", "registry", "schema")

        self.assertFalse(result)


class TestCuratedZone(unittest.TestCase):

    @patch("boto3.client")
    def test_register_athena_table_creates_new_table(self, mock_boto):
        """Test that register_athena_table calls Glue create_table with the right location."""
        mock_glue = MagicMock()
        mock_glue.exceptions.AlreadyExistsException = type("AlreadyExistsException", (Exception,), {})
        mock_boto.return_value = mock_glue

        from processing.curated_zone import register_athena_table
        register_athena_table("bucket", "s3://bucket/curated/2024/", "my_db", "my_table")

        mock_glue.create_table.assert_called_once()
        _, kwargs = mock_glue.create_table.call_args
        self.assertEqual(kwargs["DatabaseName"], "my_db")
        self.assertEqual(kwargs["TableInput"]["Name"], "my_table")
        self.assertEqual(kwargs["TableInput"]["StorageDescriptor"]["Location"], "s3://bucket/curated/2024/")

    @patch("boto3.client")
    def test_register_athena_table_updates_existing_table(self, mock_boto):
        """Test that register_athena_table falls back to update_table if the table already exists."""
        mock_glue = MagicMock()
        already_exists = type("AlreadyExistsException", (Exception,), {})
        mock_glue.exceptions.AlreadyExistsException = already_exists
        mock_glue.create_table.side_effect = already_exists()
        mock_boto.return_value = mock_glue

        from processing.curated_zone import register_athena_table
        register_athena_table("bucket", "s3://bucket/curated/2024/", "my_db", "my_table")

        mock_glue.update_table.assert_called_once()


if __name__ == "__main__":
    unittest.main()
