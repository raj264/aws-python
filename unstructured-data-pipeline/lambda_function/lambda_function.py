import boto3
import urllib.parse

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    supported_ext = ['.csv', '.json', '.xml', '.txt']
    for record in event['Records']:
        src_bucket = record['s3']['bucket']['name']
        src_key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        if any(src_key.endswith(ext) for ext in supported_ext):
            dest_key = f'staging/{src_key.split('/')[-1]}"
            s3.copy_object(Bucket=src_bucket, CopySource={'Bucket': src_bucket, 'Key': src_key}, Key=dest_key)
            s3.delete_object(Bucket=src_bucket, Key=src_key)
    return {'status': 'done'}