from pathlib import Path

from aws_cdk import (
    aws_apigateway,
    aws_dynamodb,
)
from constructs import Construct

from aws_cdk_architecture.settings import Settings
from resource_stack.aws_lambda import LambdaConstruct


class ApiGatewayConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, dragon_table: aws_dynamodb.Table) -> None:
        super().__init__(scope, construct_id)

        self._dragon_table = dragon_table
        self._api = aws_apigateway.RestApi(
            self, Settings.RESOURCE_API_GATEWAY_ID,
            rest_api_name=Settings.RESOURCE_API_GATEWAY_NAME,
            description="This service serves resources.",
            endpoint_types=[aws_apigateway.EndpointType.REGIONAL],
        )

        dragon_model = self._api.add_model(
            "DragonModel",
            model_name="DragonModel",
            content_type="application/json",
            schema=aws_apigateway.JsonSchema(
                schema=aws_apigateway.JsonSchemaVersion.DRAFT7,
                title="dragon",
                type=aws_apigateway.JsonSchemaType.OBJECT,
                properties={
                    "dragonName": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING,
                        min_length=4,
                    ),
                    "family": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING,
                        enum=["red", "blue", "green", "yellow", "black", "white"],
                    ),
                    "description": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING,
                        default="This is a dragon.",
                    ),
                    "city": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING
                    ),
                    "state": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING
                    ),
                    "country": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING
                    ),
                    "neighborhood": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING
                    ),
                    "reportingPhoneNumber": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.STRING
                    ),
                    "confirmationRequired": aws_apigateway.JsonSchema(
                        type=aws_apigateway.JsonSchemaType.BOOLEAN
                    ),
                },
                required=["dragonName", "family", "city"],
            ),
        )

        self._dragon_resource = self._api.root.add_resource("dragons")
        lambdas = LambdaConstruct(
            self, "LambdaConstruct",
            table=self._dragon_table,
        )

        self._dragon_table.grant_write_data(lambdas.create_dragon_lambda)
        self._dragon_resource.add_method(
            "POST",
            integration=aws_apigateway.LambdaIntegration(
                lambdas.create_dragon_lambda,
                integration_responses=[
                    aws_apigateway.IntegrationResponse(
                        status_code="200",
                        response_templates={
                            "application/json": "{statusCode: 200}"
                        }
                    )
                ]
            ),
            request_validator=aws_apigateway.RequestValidator(
                self, "DragonPostValidator",
                rest_api=self._api,
                validate_request_body=True,
                validate_request_parameters=False,
            ),
            request_models={"application/json": dragon_model},
        )

        self._dragon_table.grant_read_data(lambdas.list_dragons_lambda)
        self._dragon_resource.add_method(
            "GET",
            integration=aws_apigateway.LambdaIntegration(
                lambdas.list_dragons_lambda,
                integration_responses=[
                    aws_apigateway.IntegrationResponse(
                        status_code="200",
                        response_templates={
                            "application/json": "{statusCode: 200}"
                        }
                    )
                ]
            ),
        )

    @property
    def url(self) -> str:
        return self._api.url

    @property
    def dragon_resource_url(self) -> str:
        return str(Path(self._api.url) / Path(self._dragon_resource.path).name)
