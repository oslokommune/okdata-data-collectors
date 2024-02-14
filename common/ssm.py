import boto3

from .util import getenv


def get_secret(key):
    client = boto3.client("ssm", region_name=getenv("AWS_REGION"))
    resp = client.get_parameter(Name=key, WithDecryption=True)
    return resp["Parameter"]["Value"]
