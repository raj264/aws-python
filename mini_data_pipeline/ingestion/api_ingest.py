"""Module: api_ingest.py
Handles ingestion from REST, SOAP, GraphQL, and gRPC APIs."""
import requests
import boto3
import json
from zeep import Client
import grpc

def fetch_rest_api_data(url: str, headers: dict = None, params: dict = None) -> dict:
    """Fetch JSON data from a REST API endpoint.
    :param url: API URL
    :param headers: Optional HTTP headers
    :param params: Optional query params
    :return: Parsed JSON data
    """
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def fetch_soap_api_data(wsdl_url: str, method: str, **kwargs) -> dict:
    """Invoke a SOAP operation via WSDL.
    :param wsdl_url: WSDL URL
    :param method: SOAP method name
    :param kwargs: Method parameters
    :return: Response as dict
    """
    client = Client(wsdl_url)
    operation = getattr(client.service, method)
    raw_result = operation(**kwargs)
    return json.loads(json.dumps(raw_result))

def fetch_graphql_data(endpoint: str, query: str,
                       variables: dict = None, headers: dict = None) -> dict:
    """Execute a GraphQL query/mutation.
    :param endpoint: GraphQL endpoint
    :param query: GraphQL query string
    :param variables: Query variables
    :param headers: HTTP headers
    :return: GraphQL response as dict
    """
    payload = {"query": query, "variables": variables or {}}
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_grpc_data(target: str, stub_class, request) -> dict:
    """Call a gRPC service method.
    :param target: 'host:port' address
    :param stub_class: Generated Stub class
    :param request: Protobuf request message
    :return: Response as dict
    """
    channel = grpc.insecure_channel(target)
    stub = stub_class(channel)
    response = stub.MyMethod(request)
    return json.loads(json.dumps(response, default=lambda x: x.__dict__))

def upload_json_to_s3(data: dict, bucket: str, key: str) -> None:
    """Upload JSON-serializable data to S3.
    :param data: Python dict or list
    :param bucket: S3 bucket name
    :param key: S3 object key
    """
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data))
