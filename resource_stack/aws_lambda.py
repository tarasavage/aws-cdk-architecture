from aws_cdk import (
    Duration,
    aws_cloudwatch,
    aws_dynamodb,
    aws_lambda,
    aws_logs,
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

        init_duration_metric_filter = aws_logs.MetricFilter(
            self, "InitDurationMetricFilter",
            log_group=self.list_dragons.log_group,
            filter_pattern=aws_logs.FilterPattern.literal(
                f"REPORT RequestId"
            ),
            metric_name="InitDuration",
            metric_namespace="DragonService",
            metric_value="$.initDuration",
        )

        init_duration_metric = aws_cloudwatch.Metric(
            namespace="DragonService",
            metric_name="InitDuration",
            dimensions_map={"FunctionName": self.list_dragons.function_name},
            period=Duration.minutes(1),
            statistic="Average",
            color="#DD0000",
        )
        init_duration_metric_alarm = init_duration_metric.create_alarm(
            self, "InitDurationAlarm",
            evaluation_periods=1,
            threshold=500,
            alarm_description="Alarm if the init duration is over 500ms",
            alarm_name="InitDurationAlarm",
            comparison_operator=aws_cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
        )

        errors_metric = self.create_dragon.metric_errors(
            color="#FF0000",
            label="CreateDragonErrors",
            period=Duration.minutes(1),
            statistic="Sum",
        )
        errors_metric.create_alarm(
            self, "CreateDragonErrorsAlarm",
            evaluation_periods=1,
            threshold=1,
            alarm_description="Alarm if there are any errors in the CreateDragon function",
            alarm_name="CreateDragonErrorsAlarm",
            comparison_operator=aws_cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
        )

    @property
    def create_dragon_lambda(self) -> aws_lambda.Function:
        return self.create_dragon

    @property
    def list_dragons_lambda(self) -> aws_lambda.Function:
        return self.list_dragons
