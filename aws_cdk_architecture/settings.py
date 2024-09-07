import os

import boto3
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Settings class for AWS CDK Architecture."""

    @staticmethod
    def get_caller_identity() -> dict:
        sts = boto3.client("sts")
        return sts.get_caller_identity()

    @staticmethod
    def get_smm_param(key: str) -> str:
        ssm = boto3.client("ssm")
        response = ssm.get_parameter(Name=key, WithDecryption=True)

        return response.get("Parameter").get("Value")

    ACTIVITY_CONSTRUCT_ID = os.environ.get(
        "ACTIVITY_CONSTRUCT_ID", "ActivityFanoutStack"
    )
    CDK_DEFAULT_ACCOUNT = get_caller_identity().get("Account")
    CDK_DEFAULT_REGION = os.environ.get("CDK_DEFAULT_REGION", "eu-central-1")
    GITHUB_REPO = os.environ.get("GITHUB_REPO", "tarasavage/aws-cdk-architecture")
    GITHUB_BRANCH_NAME = os.environ.get("GITHUB_BRANCH_NAME", "main")
    GITHUB_CONNECTION_ARN = get_smm_param("/cdk_architecture/GITHUB_CONNECTION_ARN")
    RESOURCE_API_GATEWAY_ID = os.environ.get("RESOURCE_API_GATEWAY_ID", "ApiGatewayId")
    RESOURCE_API_GATEWAY_NAME = os.environ.get(
        "RESOURCE_API_GATEWAY_NAME", "ApiGateway"
    )
    RESOURCE_BUCKET_ID = os.environ.get(
        "RESOURCE_BUCKET_ID", "AwsCdkArchitectureBucket"
    )
    RESOURCE_BUCKET_NAME = get_smm_param("/cdk_architecture/RESOURCE_BUCKET_NAME")
    RESOURCE_STACK_NAME = os.environ.get("RESOURCE_STACK_NAME", "AwsCdkResourceStack")
    RESOURCE_CONSTRUCT_ID = os.environ.get("RESOURCE_CONSTRUCT_ID", "ResourceStack")
    RESOURCE_STACK_DEPLOY_NAME = os.environ.get(
        "RESOURCE_STACK_DEPLOY_NAME", "AwsCdkResourceStackDeploy"
    )
    PIPELINE_NAME = os.environ.get("PIPELINE_NAME", "AwsCdkPipeline")
    PIPELINE_ID = os.environ.get("PIPELINE_ID", "PipelineStack")
    CODE_PIPELINE_ID = os.environ.get("CODE_PIPELINE_ID", "CodePipeline")
    PIPELINE_WAVE_NAME = os.environ.get("PIPELINE_WAVE_NAME", "DeploymentWave")
    SHELL_STEP_ID = os.environ.get("SHELL_STEP_ID", "ShellStep")
    INIT_DURATION_THRESHOLD_MS = os.environ.get("INIT_DURATION_THRESHOLD_MS", 100)
    DRAGON_ACTIVITIES = [
        "red_dragon_activity",
        "blue_dragon_activity",
        "green_dragon_activity",
        "yellow_dragon_activity",
    ]
