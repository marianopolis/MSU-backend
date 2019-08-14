from urllib import parse
from flask import current_app
import boto3

s3_client = boto3.client('s3')

def _url(bucket, loc_constraint, name):
    return 'https://%s.s3.%s.amazonaws.com/%s' % \
        (bucket, loc_constraint, name)

def upload(key, data):
    bucket = current_app.config['S3_BUCKET']
    constraint = s3_client.get_bucket_location(Bucket=bucket)['LocationConstraint']
    s3_client.upload_fileobj(data, bucket, key)

    return _url(bucket, constraint, key)
