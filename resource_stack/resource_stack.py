from aws_cdk import (
    Stack,
    CfnOutput,
)
from constructs import Construct

from resource_stack.api_gateway import ApiGatewayConstruct


class ResourceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api_gateway = ApiGatewayConstruct(self, "ApiGatewayConstruct")

        CfnOutput(
            self, "ApiGatewayOutput",
            value=api_gateway.url,
            export_name="ApiGatewayUrl",
        )
