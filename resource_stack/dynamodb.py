from aws_cdk import (
    aws_dynamodb,
    RemovalPolicy,
)
from constructs import Construct


class DynamoDB(Construct):
    def __init__(self, scope: Construct, construct_id: str) -> None:
        super().__init__(scope, construct_id)
        self.dragon_table = aws_dynamodb.Table(
            self,
            "DragonTable",
            partition_key=aws_dynamodb.Attribute(
                name="dragonName",
                type=aws_dynamodb.AttributeType.STRING,
            ),
            sort_key=aws_dynamodb.Attribute(
                name="family",
                type=aws_dynamodb.AttributeType.STRING,
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
        self.dragon_table.add_local_secondary_index(
            index_name="DragonCityIndex",
            sort_key=aws_dynamodb.Attribute(
                name="city",
                type=aws_dynamodb.AttributeType.STRING,
            ),
            projection_type=aws_dynamodb.ProjectionType.ALL,
        )

    @property
    def table(self) -> aws_dynamodb.Table:
        return self.dragon_table
