import logging


logger = logging.getLogger(__name__)


def handler(event, context):
    logger.warning("Hello, World!")
    return {"statusCode": 200, "body": "Hello, World!"}
