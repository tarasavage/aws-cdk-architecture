from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway,
    aws_s3,
    aws_cognito,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct

from aws_cdk_architecture.settings import Settings


class ResourceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api_gateway = aws_apigateway.RestApi(
            self, Settings.RESOURCE_API_GATEWAY_ID,
            rest_api_name=Settings.RESOURCE_API_GATEWAY_NAME,
            description="This service serves resources.",
            endpoint_types=[aws_apigateway.EndpointType.REGIONAL],
        )
        user_pool = aws_cognito.UserPool(
            self, "CognitoUserPool",
            account_recovery=aws_cognito.AccountRecovery.EMAIL_ONLY,
            mfa=aws_cognito.Mfa.OFF,
            password_policy=aws_cognito.PasswordPolicy(
                min_length=7,
                require_lowercase=True,
                require_digits=True,
            ),
            sign_in_aliases=aws_cognito.SignInAliases(
                email=True,
                username=True,
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )
        auth = aws_apigateway.CognitoUserPoolsAuthorizer(
            self, "CognitoAuthorizer",
            cognito_user_pools=[user_pool],
            authorizer_name="CognitoAuthorizer",
            results_cache_ttl=Duration.minutes(5),
        )

        resource = api_gateway.root.add_resource("hello")
        resource.add_method(
            "POST",
            aws_apigateway.MockIntegration(
                integration_responses=[
                    aws_apigateway.IntegrationResponse(
                        status_code="200",
                        response_templates={
                            "application/json": '{"message": "hello world"}'
                        },
                    )
                ]
            ),
            authorizer=auth,
            method_responses=[
                aws_apigateway.MethodResponse(
                    status_code="200",
                    response_models={
                        "application/json": aws_apigateway.Model.EMPTY_MODEL
                    },
                )
            ],
        )

        bucket = aws_s3.Bucket(
            self, Settings.RESOURCE_BUCKET_ID,
            bucket_name=Settings.RESOURCE_BUCKET_NAME,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
            versioned=False,
            encryption=aws_s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        CfnOutput(
            self, "BucketOutput",
            value=bucket.bucket_name,
            export_name="BucketName",
        )
        CfnOutput(
            self, "ApiGatewayOutput",
            value=api_gateway.url,
            export_name="ApiGatewayUrl",
        )
