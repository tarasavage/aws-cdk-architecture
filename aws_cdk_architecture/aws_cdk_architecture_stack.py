from aws_cdk import (
    Stack,
    Stage,
    Environment,
    pipelines,
    aws_codepipeline,
    aws_iam as iam,
)
from constructs import Construct

from aws_cdk_architecture.settings import Settings
from resource_stack.resource_stack import ResourceStack


class DeployStage(Stage):
    def __init__(
        self, scope: Construct, construct_id: str, env: Environment, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)
        ResourceStack(
            self,
            construct_id=Settings.RESOURCE_CONSTRUCT_ID,
            env=env,
            stack_name=Settings.RESOURCE_STACK_NAME,
        )


class AwsCdkArchitectureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ssm_policy = iam.PolicyStatement(
            actions=["ssm:GetParameter"],
            resources=[
                (
                    f"arn:aws:ssm:{Settings.CDK_DEFAULT_REGION}:{Settings.CDK_DEFAULT_ACCOUNT}:"
                    f"parameter/cdk_architecture/*"
                )
            ],
        )

        git_input = pipelines.CodePipelineSource.connection(
            repo_string=Settings.GITHUB_REPO,
            branch=Settings.GITHUB_BRANCH_NAME,
            connection_arn=Settings.GITHUB_CONNECTION_ARN,
        )

        code_pipeline = aws_codepipeline.Pipeline(
            self, Settings.PIPELINE_ID,
            pipeline_name=Settings.PIPELINE_NAME,
            cross_account_keys=False,
        )

        synth_step = pipelines.ShellStep(
            id=Settings.SHELL_STEP_ID,
            install_commands=["pip install -r requirements.txt"],
            commands=["npx cdk synth"],
            input=git_input,
        )

        pipeline = pipelines.CodePipeline(
            self, Settings.CODE_PIPELINE_ID,
            self_mutation=True,
            code_pipeline=code_pipeline,
            synth=synth_step,
            code_build_defaults=pipelines.CodeBuildOptions(
                role_policy=[ssm_policy]
            )
        )

        deployment_wave = pipeline.add_wave(Settings.PIPELINE_WAVE_NAME)

        deployment_wave.add_stage(
            DeployStage(
                self, Settings.RESOURCE_STACK_DEPLOY_NAME,
                env=(
                    Environment(
                        account=Settings.CDK_DEFAULT_ACCOUNT,
                        region=Settings.CDK_DEFAULT_REGION,
                    )
                ),
            ),
            post=[pipelines.ManualApprovalStep("ApproveResourceDeployment")]
        )
