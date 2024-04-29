from datetime import datetime

import boto3
from botocore.config import Config

my_config = Config(
    region_name = 'eu-central-1'
)

# Get the service resource.

session = boto3.Session()

dynamodb = session.resource('dynamodb', config=my_config)
scores_table = dynamodb.Table('IrisExtended')