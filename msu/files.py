"""Utility module for file handling.

Using AWS S3, we can upload and download files. To
use this module, ensure boto3 is properly configured
by following the instructions at

[https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html].

Additionally, ensure the relevant environment variables in `config.py`
are set.
"""

from urllib import parse
import boto3

from flask import (
    current_app,
    flash,
    request
)


s3_client = boto3.client('s3')

def _url(bucket, loc_constraint, name):
    return 'https://%s.s3.%s.amazonaws.com/%s' % \
        (bucket, loc_constraint, name)

def _upload(key, data, bucket):

    constraint = s3_client.get_bucket_location(Bucket=bucket)['LocationConstraint']
    s3_client.upload_fileobj(data, bucket, key)

    return _url(bucket, constraint, key)

def upload_file(key, data):
    bucket = current_app.config['S3_BUCKET_FILES']
    return _upload(key, data, bucket)

def delete_file(key):
    bucket = current_app.config['S3_BUCKET_FILES']
    s3_client.delete_object(Bucket=bucket, Key=key)

def upload_image(key,data):
    bucket = current_app.config['S3_BUCKET_IMAGES']
    return _upload(key, data, bucket)
