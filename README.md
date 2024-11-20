## Automate File Handling With Python & AWS S3

## Few notes on Creating IAM users:
* Create a user
* Enable programmatic access
* Add user to a group with the desired permissions
* Copy access and secret access keys

## Install Dependencies
    pip3 install -r requirements.txt

## Run the Script
    python automatic_s3_uploader.py

## Features
- Automatically uploads all files from a local directory (including subdirectories).
- Skips files already present in the S3 bucket.
- Allows user input for directory path, S3 bucket name, and optional prefix.
- Uses a JSON file to securely store AWS credentials.