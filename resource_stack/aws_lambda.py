from aws_cdk import (
    aws_dynamodb,
    aws_lambda,
)
from constructs import Construct


class LambdaConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, table: aws_dynamodb.Table) -> None:
        super().__init__(scope, construct_id)

        self.create_dragon = aws_lambda.Function(
            self, "CreateDragonLambda",
            handler="create_dragon.lambda_handler",
            code=aws_lambda.Code.from_asset("lambda/endpoints/create_dragon/"),
            environment={"TABLE_NAME": table.table_name},
            runtime=aws_lambda.Runtime.PYTHON_3_11,
        )

        self.list_dragons = aws_lambda.Function(
            self, "ListDragonsLambda",
            handler="list_dragons.lambda_handler",
            code=aws_lambda.Code.from_asset("lambda/endpoints/list_dragons/"),
            environment={"TABLE_NAME": table.table_name},
            runtime=aws_lambda.Runtime.PYTHON_3_11,
        )

    @property
    def create_dragon_lambda(self) -> aws_lambda.Function:
        return self.create_dragon

    @property
    def list_dragons_lambda(self) -> aws_lambda.Function:
        return self.list_dragons
