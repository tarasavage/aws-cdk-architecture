from aws_cdk import (
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subscriptions,
    Stack,
    RemovalPolicy,
    Duration,
)
from constructs import Construct


class DragonActivityFanoutStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, activities: list[str], **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._activities = activities
        self._activity_topic = self._create_topic(
            "DragonActivityTopic", "Dragon Activity Topic"
        )
        self._activity_queues = self._create_activity_queues(self.activities)

        self._subscribe_multiple_queues_to_activity_topic(
            [queue[0] for queue in self._activity_queues.values()]
        )

    @property
    def activity_topic(self) -> sns.Topic:
        return self._activity_topic

    @property
    def activities(self) -> list[str]:
        return self._activities

    @property
    def activity_and_dead_letter_queues(self) -> dict[str, tuple[sqs.Queue, sqs.Queue]]:
        return self._activity_queues

    @property
    def activity_queues(self) -> dict[sqs.Queue]:
        return self._get_queues()

    @property
    def activity_dead_letter_queues(self) -> dict[sqs.Queue]:
        return self._get_queues(dead_letter_queue=True)

    def get_activity_queue_by_name(self, queue_name: str) -> sqs.Queue:
        return self.activity_queues[queue_name]

    def get_dead_letter_queue_by_name(self, queue_name: str) -> sqs.Queue:
        return self.activity_dead_letter_queues[queue_name]

    def _get_queues(self, dead_letter_queue: bool = False) -> dict[sqs.Queue]:
        index = int(not dead_letter_queue)

        return {
            activity: queues[index]
            for activity, queues in self.activity_and_dead_letter_queues.items()
        }

    def _subscribe_multiple_queues_to_activity_topic(
        self, queues: list[sqs.Queue]
    ) -> None:
        for queue in queues:
            self._activity_topic.add_subscription(
                sns_subscriptions.SqsSubscription(queue)
            )

    def _subscribe_to_activity_topic(self, queue: sqs.Queue) -> None:
        self._activity_topic.add_subscription(sns_subscriptions.SqsSubscription(queue))

    def _create_activity_queues(
        self, activities: list[str]
    ) -> dict[str, tuple[sqs.Queue, sqs.Queue]]:
        return {
            activity: self._create_queue_with_dql(activity) for activity in activities
        }

    def _create_queue(self, queue_name: str, **kwargs) -> sqs.Queue:
        return sqs.Queue(
            self,
            queue_name,
            content_based_deduplication=True,
            queue_name=queue_name,
            visibility_timeout=Duration.seconds(30),
            retention_period=Duration.days(14),
            fifo=True,
            receive_message_wait_time=20,
            removal_policy=RemovalPolicy.DESTROY,
            **kwargs,
        )

    def _create_queue_with_dql(self, queue_name: str) -> tuple[sqs.Queue, sqs.Queue]:
        dlq = sqs.DeadLetterQueue(
            self,
            queue=self._create_queue(f"{queue_name}DlqQueue.fifo"),
            max_receive_count=3,
        )

        main_queue = self._create_queue(
            f"{queue_name}Queue.fifo", dead_letter_queue=dlq
        )
        return main_queue, dlq

    def _create_topic(self, topic_name: str, display_name: str) -> sns.Topic:
        return sns.Topic(
            self,
            topic_name,
            display_name=display_name,
            fifo=True,
            content_based_deduplication=True,
            message_retention_period_in_days=14,
            topic_name=f"{topic_name}.fifo",
        )
