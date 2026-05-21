from confluent_kafka.admin import AdminClient, NewTopic


class KafkaAdmin:

    def __init__(self, bootstrap_servers: str) -> None:
        # Kafka broker address (e.g. localhost:9092)
        self.bootstrap_servers = bootstrap_servers

        # Admin client used for Kafka operations
        self.admin_client = AdminClient(
            conf={'bootstrap.servers': self.bootstrap_servers}
        )

    def topic_exists(self, topic_name: str) -> bool:
        # Fetch metadata for all topics from Kafka cluster
        cluster_metadata = self.admin_client.list_topics()

        # Check if topic exists in cluster
        return topic_name in cluster_metadata.topics.keys()

    def create_topic(self, topic_name: str) -> None:

        # Create topic only if it does not already exist
        if not self.topic_exists(topic_name):

            # Define new topic
            new_topic = NewTopic(topic_name)

            # Kafka allows creating multiple topics at once
            self.admin_client.create_topics([new_topic])

            print(f"Topic created: {topic_name}")

        else:
            print(f"Topic already exists: {topic_name}")