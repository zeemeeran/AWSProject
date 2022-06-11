import boto3
#import logging
from botocore.exceptions import ClientError
import os



# #Creating Session With Boto3.
# session = boto3.Session(
# aws_access_key_id='<your_access_key_id>',
# aws_secret_access_key='<your_secret_access_key>'
# )


# s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                   #   aws_secret_access_key=SECRET_KEY)


def upload(fname):
    s3_client = boto3.client('s3')
    path = 'static/files/' + fname
    try:
        response = s3_client.upload_file(path, 'student-pictures', fname)
    except ClientError as e:
        #logging.error(e)
        return False
    return True
