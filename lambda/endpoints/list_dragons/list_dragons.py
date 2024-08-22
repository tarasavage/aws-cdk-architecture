import os
import boto3
import logging
import json
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


TABLE_NAME = os.environ.get("TABLE_NAME", "DragonTable")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    dragons = []
    start_key = None
    try:
        done = False
        while not done:
            if start_key:
                response = table.scan(ExclusiveStartKey=start_key)
            else:
                response = table.scan()
            dragons.extend(response.get("Items", []))
            start_key = response.get("LastEvaluatedKey", None)
            done = start_key is None
    except ClientError as err:
        logger.error(
            "Couldn't scan for dragons. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise err

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(dragons)
    }
