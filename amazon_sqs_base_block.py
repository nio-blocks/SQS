import boto3
from enum import Enum

from nio.block.base import Block
from nio.properties import (VersionProperty, PropertyHolder, StringProperty,
                            ObjectProperty, SelectProperty)
from nio.util.discovery import not_discoverable


class Regions(Enum):
    us_east_1 = "us-east-1"
    us_east_2 = "us-east-2"
    us_west_1 = "us-west-1"
    us_west_2 = "us-west-2"
    ca_central_1 = "ca_central_1"
    eu_west_1 = "eu-west-1"
    eu_west_2 = "eu-west-2"
    eu_central_1 = "eu-central-1"
    ap_northeast_1 = "ap-northeast-1"
    ap_northeast_2 = "ap-northeast-2"
    ap_southeast_1 = "ap-southeast-1"
    ap_southeast_2 = "ap-southeast-2"
    ap_south_1 = "ap-south-1"
    sa_east_1 = "sa-east-1"


class AWSCreds(PropertyHolder):
    region_name = SelectProperty(
        Regions,
        title="Region Name",
        default=Regions.us_east_2
    )
    aws_access_key_id = StringProperty(
        title="Access Key ID", default="", allow_none=False)
    aws_secret_access_key = StringProperty(
        title="Secret Access Key", default="", allow_none=False)
    aws_session_token = StringProperty(
        title="Session Token", default="", allow_none=True)


@not_discoverable
class SQSBase(Block):
    """ This is the base block for integrating n.io with AWS SQS"""
    version = VersionProperty("1.0.0")
    creds = ObjectProperty(
        AWSCreds, title="AWS Credentials", default=AWSCreds())

    # Queue to connect to
    queue_url = StringProperty(title="Queue URL", default="")

    def __init__(self):
        self.client = None
        super().__init__()

    def configure(self, context):
        super().configure(context)
        self.client = boto3.client(
            'sqs',
            region_name=self.creds().region_name().value,
            aws_access_key_id=self.creds().aws_access_key_id(),
            aws_secret_access_key=self.creds().aws_secret_access_key(),
            aws_session_token=self.creds().aws_secret_access_key())
