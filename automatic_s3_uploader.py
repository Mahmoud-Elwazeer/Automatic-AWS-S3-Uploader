# from secrets import access_key, secret_access_key

import boto3
import os
import json


def load_credentials(credential_file):
    """
    Load AWS credentials from a JSON file.

    :param credential_file: Path to the JSON file containing AWS credentials.
    :return: A dictionary with AWS credentials.
    """
    try:
        with open(credential_file, 'r') as file:
            credentials = json.load(file)
            return credentials
    except FileNotFoundError:
        print(f"Error: Credential file {credential_file} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Credential file {credential_file} is not valid JSON.")
        return None


def file_exists_in_s3(bucket_name, s3_key, s3_client):
    """
    Check if a file already exists in the S3 bucket.

    :param bucket_name: Name of the S3 bucket.
    :param s3_key: The key (path) of the file in the S3 bucket.
    :param s3_client: Boto3 S3 client.
    :return: True if the file exists, False otherwise.
    """
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_key)
        for obj in response.get('Contents', []):
            if obj['Key'] == s3_key:
                return True
        return False
    except Exception as e:
        print(f"Error checking existence of {s3_key}: {e}")
        return False



def upload_to_s3(file_path, bucket_name, s3_key, credentials):
    """
    Uploads a file to an S3 bucket.

    :param file_path: Path to the file to upload.
    :param bucket_name: Name of the target S3 bucket.
    :param s3_key: The key (path) in the S3 bucket where the file will be stored.
    :param credentials: AWS credentials as a dictionary.
    :return: None
    """
    try:
        # Initialize the S3 client using credentials
        s3_client = boto3.client(
            's3',
            aws_access_key_id=credentials['access_key'],
            aws_secret_access_key=credentials['secret_access_key'],
        )

        if file_exists_in_s3(bucket_name, s3_key, s3_client):
            print(f"File already exists in S3, skipping: {s3_key}")
            return

        # Upload the file
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Upload Successful: {file_path} to s3://{bucket_name}/{s3_key}")

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def auto_upload(directory_path, bucket_name, s3_prefix, credentials):
    """
    Automatically uploads all files in a directory to an S3 bucket.

    :param directory_path: Path to the directory containing files to upload.
    :param bucket_name: Name of the target S3 bucket.
    :param s3_prefix: Optional prefix for keys in the S3 bucket.
    :param credentials: AWS credentials as a dictionary.
    :return: None
    """
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        return

    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Determine the S3 key
            relative_path = os.path.relpath(file_path, directory_path)
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")  # Ensure Unix-style paths
            upload_to_s3(file_path, bucket_name, s3_key, credentials)

if __name__ == "__main__":
    # Load AWS credentials from the file
    CREDENTIAL_FILE = "aws_credentials.json"
    credentials = load_credentials(CREDENTIAL_FILE)

    if credentials:
        directory_to_upload = input("Enter the path of the directory to upload: ").strip()
        s3_bucket_name = input("Enter the name of the S3 bucket: ").strip()
        s3_prefix = input("Enter the optional S3 prefix (leave empty for none): ").strip()

        auto_upload(directory_to_upload, s3_bucket_name,s3_prefix, credentials)