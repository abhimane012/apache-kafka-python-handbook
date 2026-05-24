from confluent_kafka.admin import AdminClient, NewTopic


class KafkaAdmin:
    def __init__(self, bootstrap_servers: str) -> None:

        # Kafka broker address
        # Example: localhost:9092
        self.bootstrap_servers = bootstrap_servers

        # Create Kafka admin client
        # Used for topic operations
        self.admin_client = AdminClient({"bootstrap.servers": self.bootstrap_servers})

    def topic_exists(self, topic_name: str) -> bool:

        # Fetch cluster metadata
        cluster_metadata = self.admin_client.list_topics()

        # Check whether topic exists
        return topic_name in cluster_metadata.topics

    def create_topic(self, topic_name: str, partitions: int = 1) -> None:

        # Create topic only if
        # it does not exist
        if not self.topic_exists(topic_name):
            # Define topic settings
            new_topic = NewTopic(topic=topic_name, num_partitions=partitions)

            # Kafka accepts a list
            # because multiple topics
            # can be created together
            self.admin_client.create_topics([new_topic],)

            print(f"Topic created: {topic_name}")

        else:
            print(f"Topic already exists: {topic_name}")


if __name__ == "__main__":
    bootstrap_servers = "localhost:19092"

    topic_name = "test-topic"

    kafka_admin = KafkaAdmin(bootstrap_servers)

    kafka_admin.create_topic(topic_name, partitions=2)
