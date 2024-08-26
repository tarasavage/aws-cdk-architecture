from aws_cdk import (
    Stack,
    CfnOutput,
)
from constructs import Construct

from resource_stack.api_gateway import ApiGatewayConstruct
from resource_stack.auth import CognitoConstruct, CognitoClientConstruct
from resource_stack.dynamodb import DynamoDB


class ResourceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dragon_table = DynamoDB(self, "DynamoDBConstruct")
        cognito_construct = CognitoConstruct(self, "CognitoConstruct")
        api_gateway = ApiGatewayConstruct(self, "ApiGatewayConstruct", dragon_table.table)
        cognito_client_construct = CognitoClientConstruct(
            self, "CognitoClientConstruct",
            user_pool=cognito_construct.user_pool,
            callback_urls=[api_gateway.dragon_resource_url],
        )

        CfnOutput(
            self, "DynamoDBTableName",
            value=dragon_table.table.table_name,
            export_name="DynamoDBTableName",
        )
        CfnOutput(
            self, "ApiGatewayOutput",
            value=api_gateway.url,
            export_name="ApiGatewayUrl",
        )
