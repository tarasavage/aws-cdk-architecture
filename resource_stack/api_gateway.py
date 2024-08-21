from aws_cdk import (
    aws_apigateway,
    aws_dynamodb,
)
from constructs import Construct

from aws_cdk_architecture.settings import Settings
from resource_stack.aws_lambda import LambdaConstruct

GET_DRAGON_LIST_TEMPLATE = """
[
  #if( $input.params('family') == "red" )
    {
      "description_str":"Xanya is the fire tribe's banished general. She broke ranks and has been wandering ever since.",
      "dragon_name_str":"Xanya",
      "family_str":"red",
      "location_city_str":"las vegas",
      "location_country_str":"usa",
      "location_neighborhood_str":"e clark ave",
      "location_state_str":"nevada"
    },
    {
      "description_str":"Eislex flies with the fire sprites. He protects them and is their guardian.",
      "dragon_name_str":"Eislex",
      "family_str":"red",
      "location_city_str":"st. cloud",
      "location_country_str":"usa",
      "location_neighborhood_str":"breckenridge ave",
      "location_state_str":"minnesota"
    }
  #elseif( $input.params('family') == "blue" )
    {
      "description_str":"Protheus is a wise and ancient dragon that serves on the grand council in the sky world. He uses his power to calm those near him.",
      "dragon_name_str":"Protheus",
      "family_str":"blue",
      "location_city_str":"brandon",
      "location_country_str":"usa",
      "location_neighborhood_str":"e morgan st",
      "location_state_str":"florida"
    }
  #elseif( $input.params('dragonName') == "Atlas" )
    {
      "description_str":"From the northern fire tribe, Atlas was born from the ashes of his fallen father in combat. He is fearless and does not fear battle.",
      "dragon_name_str":"Atlas",
      "family_str":"red",
      "location_city_str":"anchorage",
      "location_country_str":"usa",
      "location_neighborhood_str":"w fireweed ln",
      "location_state_str":"alaska"
    }
  #else
    {
      "description_str":"From the northern fire tribe, Atlas was born from the ashes of his fallen father in combat. He is fearless and does not fear battle.",
      "dragon_name_str":"Atlas",
      "family_str":"red",
      "location_city_str":"anchorage",
      "location_country_str":"usa",
      "location_neighborhood_str":"w fireweed ln",
      "location_state_str":"alaska"
    },
    {
      "description_str":"Protheus is a wise and ancient dragon that serves on the grand council in the sky world. He uses his power to calm those near him.",
      "dragon_name_str":"Protheus",
      "family_str":"blue",
      "location_city_str":"brandon",
      "location_country_str":"usa",
      "location_neighborhood_str":"e morgan st",
      "location_state_str":"florida"
    },
    {
      "description_str":"Xanya is the fire tribe's banished general. She broke ranks and has been wandering ever since.",
      "dragon_name_str":"Xanya",
      "family_str":"red",
      "location_city_str":"las vegas",
      "location_country_str":"usa",
      "location_neighborhood_str":"e clark ave",
      "location_state_str":"nevada"
    },
    {
      "description_str":"Eislex flies with the fire sprites. He protects them and is their guardian.",
      "dragon_name_str":"Eislex",
      "family_str":"red",
      "location_city_str":"st. cloud",
      "location_country_str":"usa",
      "location_neighborhood_str":"breckenridge ave",
      "location_state_str":"minnesota"
    }
  #end
]
"""


class ApiGatewayConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, dragon_table: aws_dynamodb.Table) -> None:
        super().__init__(scope, construct_id)

        self.dragon_table = dragon_table
        self.api = aws_apigateway.RestApi(
            self, Settings.RESOURCE_API_GATEWAY_ID,
            rest_api_name=Settings.RESOURCE_API_GATEWAY_NAME,
            description="This service serves resources.",
            endpoint_types=[aws_apigateway.EndpointType.REGIONAL],
        )

        dragon_model = self.api.add_model(
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

        dragon_resource = self.api.root.add_resource("dragons")
        create_dragon_lambda = LambdaConstruct(
            self, "LambdaConstruct",
            table=self.dragon_table
        )
        self.dragon_table.grant_write_data(create_dragon_lambda.function)
        dragon_resource.add_method(
            "POST",
            integration=aws_apigateway.LambdaIntegration(
                create_dragon_lambda.function,
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
                rest_api=self.api,
                validate_request_body=True,
                validate_request_parameters=False,
            ),
            request_models={"application/json": dragon_model},
        )


        # MOCK INTEGRATION
        dragons_resource_v2 = self.api.root.add_resource("dragons_v2")
        dragons_resource_v2.add_method(
            "GET",
            integration=aws_apigateway.MockIntegration(
                integration_responses=[
                    aws_apigateway.IntegrationResponse(
                        status_code="200",
                        response_templates={
                            "application/json": GET_DRAGON_LIST_TEMPLATE
                        },
                    )
                ],
                request_templates={"application/json": '{"statusCode": 200}'},
            ),
            method_responses=[aws_apigateway.MethodResponse(status_code="200")],
        )
        dragons_resource_v2.add_method(
            "POST",
            integration=aws_apigateway.MockIntegration(
                integration_responses=[
                    aws_apigateway.IntegrationResponse(
                        status_code="200",
                        response_templates={
                            "application/json": """
                                #set($body = $context.requestOverride.path.body)
                                {
                                    "statusCode": 200,
                                    "body": $body
                                }
                                """
                        },
                    )
                ],
                request_templates={
                    "application/json": """
                    #set($context.requestOverride.path.body = $input.body)
                    {
                        "statusCode": 200
                    }
                    """
                },
            ),
            method_responses=[aws_apigateway.MethodResponse(status_code="200")],
            request_validator=aws_apigateway.RequestValidator(
                self, "DragonPostValidatorV2",
                rest_api=self.api,
                validate_request_body=True,
                validate_request_parameters=False,
            ),
            request_models={"application/json": dragon_model},
        )

    @property
    def url(self) -> str:
        return self.api.url
