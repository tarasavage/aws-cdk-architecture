import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    CDK_DEFAULT_ACCOUNT = os.environ.get("CDK_DEFAULT_ACCOUNT")
    CDK_DEFAULT_REGION = os.environ.get("CDK_DEFAULT_REGION")
    GITHUB_REPO = os.environ.get("GITHUB_REPO")
    GITHUB_BRANCH_NAME = os.environ.get("GITHUB_BRANCH_NAME")
    GITHUB_CONNECTION_ARN = os.environ.get("GITHUB_CONNECTION_ARN")
    RESOURCE_API_GATEWAY_ID = os.environ.get("RESOURCE_API_GATEWAY_ID")
    RESOURCE_API_GATEWAY_NAME = os.environ.get("RESOURCE_API_GATEWAY_NAME")
    RESOURCE_BUCKET_ID = os.environ.get("RESOURCE_BUCKET_ID")
    RESOURCE_BUCKET_NAME = os.environ.get("RESOURCE_BUCKET_NAME")
    RESOURCE_STACK_NAME = os.environ.get("RESOURCE_STACK_NAME")
    RESOURCE_CONSTRUCT_ID = os.environ.get("RESOURCE_CONSTRUCT_ID")
    RESOURCE_STACK_DEPLOY_NAME = os.environ.get("RESOURCE_STACK_DEPLOY_NAME")
    PIPELINE_NAME = os.environ.get("PIPELINE_NAME")
    PIPELINE_ID = os.environ.get("PIPELINE_ID")
    CODE_PIPELINE_ID = "CodePipeline"
    PIPELINE_WAVE_NAME = os.environ.get("PIPELINE_WAVE_NAME")
    SHELL_STEP_ID = os.environ.get("SHELL_STEP_ID")
