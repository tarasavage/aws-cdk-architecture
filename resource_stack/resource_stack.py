import os

from aws_cdk import (
    Stack,
    aws_apigateway,
    aws_s3,
)
from constructs import Construct

from aws_cdk_architecture.settings import Settings


class ResourceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api_gateway = aws_apigateway.RestApi(
            self,
            Settings.RESOURCE_API_GATEWAY_ID,
            rest_api_name=Settings.RESOURCE_API_GATEWAY_NAME,
            description="This service serves resources.",
            endpoint_types=[aws_apigateway.EndpointType.REGIONAL],
        )

        resource = api_gateway.root.add_resource("hello")
        resource.add_method("GET")

        bucket = aws_s3.Bucket(
            self,
            Settings.RESOURCE_BUCKET_ID,
            bucket_name=Settings.RESOURCE_BUCKET_NAME,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            versioned=False,
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
        )
