"""Utility module for file handling.

Using AWS S3, we can upload and download files. To
use this module, ensure boto3 is properly configured
by following the instructions at

[https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html].

Additionally, ensure the relevant environment variables in `config.py`
are set.
"""

import pathlib
import time

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

    return (key, _url(bucket, constraint, key))

def upload(filename, data):
    bucket = current_app.config['S3_BUCKET']

    # The key is generated using <current timestamp>.<extension>.
    # This ensures (or tries to) that no two files share a key.
    name = int(time.time()*1000) # ms since epoch
    ext = ''.join(pathlib.Path(filename).suffixes)
    key = f'{name}{ext}'

    return _upload(key, data, bucket)

def delete(key):
    bucket = current_app.config['S3_BUCKET']
    s3_client.delete_object(Bucket=bucket, Key=key)
