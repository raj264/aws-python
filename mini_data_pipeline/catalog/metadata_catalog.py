"""Module: metadata_catalog.py
Automates metadata management with Glue crawlers and Lake Formation governance."""
import boto3

def run_glue_crawler(crawler_name: str):
    """Start an AWS Glue crawler to update the Data Catalog."""
    glue = boto3.client('glue')
    glue.start_crawler(Name=crawler_name)

def grant_lakeformation_permissions(resource_arn: str, principal: str, permissions: list):
    """Grant Lake Formation permissions on a database/table resource to a principal."""
    lf = boto3.client('lakeformation')
    lf.grant_permissions(
        Principal={'DataLakePrincipalIdentifier': principal},
        Resource={'DataLocation': {'ResourceArn': resource_arn}},
        Permissions=permissions,
    )
