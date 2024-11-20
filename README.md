## Automate File Handling With Python & AWS S3

## Few notes on Creating IAM users:
* Create a user
* Enable programmatic access
* Add user to a group with the desired permissions
* Copy access and secret access keys

## Install Dependencies
    pip3 install -r requirements.txt

## Prerequisites
1. **Python**.
2. **Install Dependencies**:
     ```bash
     pip3 install -r requirements.txt
     ```
3. **AWS Account**:
   - An AWS account is required with access to S3.
   - Create or use an existing S3 bucket.

4. **AWS Credentials File**:
   - Edit Credentials in a file named `aws_credentials.json`:
     ```json
     {
         "aws_access_key_id": "your-access-key-id",
         "aws_secret_access_key": "your-secret-access-key",
     }
     ```

---


## Run the Script
    python automatic_s3_uploader.py

## Features
- Automatically uploads all files from a local directory (including subdirectories).
- Skips files already present in the S3 bucket.
- Allows user input for directory path, S3 bucket name, and optional prefix.
- Uses a JSON file to securely store AWS credentials.