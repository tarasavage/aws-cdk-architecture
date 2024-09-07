import os
import json
import logging
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

TABLE_NAME = os.environ.get("TABLE_NAME", "DragonTable")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    try:
        dragon = json.loads(event["body"])
        response = table.put_item(Item=dragon)
        logger.debug(f"Item added successfully: {response}")
        return {"statusCode": 200, "body": json.dumps("Item added successfully")}
    except ClientError as e:
        error_message = e.response["Error"]["Message"]
        logger.error(f"ClientError: {error_message}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error adding item to DynamoDB: {error_message}"),
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps("Unexpected error occurred")}
