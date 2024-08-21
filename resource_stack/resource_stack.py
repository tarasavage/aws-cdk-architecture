from aws_cdk import (
    Stack,
    CfnOutput,
)
from constructs import Construct

from resource_stack.api_gateway import ApiGatewayConstruct
from resource_stack.dynamodb import DynamoDB
from resource_stack.aws_lambda import LambdaConstruct


class ResourceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dragon_table = DynamoDB(self, "DynamoDBConstruct")
        api_gateway = ApiGatewayConstruct(self, "ApiGatewayConstruct", dragon_table.table)
        create_dragon_lambda = LambdaConstruct(
            self, "LambdaConstruct",
            table=dragon_table.table
        )
        dragon_table.table.grant_write_data(create_dragon_lambda.function)

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
