"""Module: ftp_ingest.py
Handles batch ingestion from FTP/SFTP into S3."""
import ftplib
import boto3

def download_from_ftp(host: str, port: int, username: str, password: str,
                      remote_path: str, local_path: str) -> None:
    """Download a file from FTP/SFTP to a local path.
    :param host: FTP server hostname
    :param port: FTP server port
    :param username: FTP login username
    :param password: FTP login password
    :param remote_path: File path on FTP server
    :param local_path: Destination path locally
    """
    ftp = ftplib.FTP()
    ftp.connect(host, port)
    ftp.login(username, password)
    with open(local_path, 'wb') as f:
        ftp.retrbinary(f'RETR {remote_path}', f.write)
    ftp.quit()

def upload_to_s3(local_path: str, bucket: str, key: str) -> None:
    """Upload a local file to S3.
    :param local_path: Local file path
    :param bucket: S3 bucket name
    :param key: S3 object key
    """
    s3 = boto3.client('s3')
    s3.upload_file(local_path, bucket, key)
