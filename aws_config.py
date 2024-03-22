import os

import boto3

os.environ.setdefault('AWS_ACCESS_KEY_ID', os.environ.get('AWS_ACCESS_KEY_ID'))
os.environ.setdefault('AWS_SECRET_ACCESS_KEY', os.environ.get('AWS_SECRET_ACCESS_KEY'))

session = boto3.Session()

s3_client = session.client('s3')

lambda_client = session.client('lambda')

apigateway_client = session.client('apigateway')

sns_client = session.client('sns')

s3_resource = session.resource('s3')

dynamodb = session.resource('dynamodb')

cache = session.resource('redis', service_name='redis-001')
