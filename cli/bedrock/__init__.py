import boto3

def create_sdk_client(service_name):
  return boto3.client(service_name=service_name, region_name='us-west-2')
