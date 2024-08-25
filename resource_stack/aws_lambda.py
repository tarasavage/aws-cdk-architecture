from aws_cdk import (
    Duration,
    aws_cloudwatch,
    aws_dynamodb,
    aws_lambda,
    aws_logs,
)
from constructs import Construct

from aws_cdk_architecture.settings import Settings


class LambdaConstruct(Construct):
    def __init__(
        self, scope: Construct, construct_id: str, table: aws_dynamodb.Table
    ) -> None:
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
                f"[..., InitDuration, coldStart>{Settings.INIT_DURATION_THRESHOLD_MS}, remaining]"
            ),
            metric_namespace="DragonService",
            metric_name="InitDuration",
            metric_value="1",
            default_value=0,
        )
        init_duration_metric_alarm = aws_cloudwatch.Alarm(
            self, "InitDurationAlarm",
            metric=init_duration_metric_filter.metric(
                period=Duration.minutes(1),
                color="#FF0000",
                label="InitDurationMetric",
                statistic="Sum",
            ),
            evaluation_periods=1,
            threshold=1,
            alarm_description="Alarm if there are any init durations over 100ms in the ListDragons function",
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
