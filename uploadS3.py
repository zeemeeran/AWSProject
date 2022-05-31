import boto3
#import logging
from botocore.exceptions import ClientError
import os

def upload(fname):
    s3_client = boto3.client('s3')
    path = 'static/files/' + fname
    try:
        response = s3_client.upload_file(path, 'student-pictures', fname)
    except ClientError as e:
        #logging.error(e)
        return False
    return True