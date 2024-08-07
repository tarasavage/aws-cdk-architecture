import aws_cdk as cdk

from aws_cdk_architecture.aws_cdk_architecture_stack import AwsCdkArchitectureStack
from aws_cdk_architecture.settings import Settings

app = cdk.App()
AwsCdkArchitectureStack(
    app, "AwsCdkArchitectureStack",
    env=cdk.Environment(
        account=Settings.CDK_DEFAULT_ACCOUNT,
        region=Settings.CDK_DEFAULT_REGION,
    ),
    stack_name=Settings.RESOURCE_STACK_NAME,
)

cdk.Tags.of(app).add(key="feature", value="aws-cdk-architecture")
cdk.Tags.of(app).add(key="contact", value="taras.panasiuk.work@gmail.com")
cdk.Tags.of(app).add(key="team", value="solo-ride")

app.synth()
