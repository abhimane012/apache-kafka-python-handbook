from confluent_kafka.admin import AdminClient, NewTopic


class Admin:

    def __init__(self, bootstrap_server: str) -> None:
        # Store Kafka broker address
        # Example: localhost:9092
        self.bootstrap_server = bootstrap_server

        # Create Kafka Admin client
        # This client is used for admin operations
        # like creating topics, deleting topics, etc.
        self.admin = AdminClient(
            {'bootstrap.servers': self.bootstrap_server}
        )

    def topic_exists(self, topic: str) -> bool:
        # Get metadata for all topics from Kafka
        all_topics = self.admin.list_topics()

        # Check whether the topic exists
        # in the list of available topics
        return topic in all_topics.topics.keys()

    def create_topic(self, topic: str) -> None:

        # Create topic only if it does not exist
        if not self.topic_exists(topic):

            # Create topic object
            new_topics = NewTopic(topic)

            # Kafka accepts a list because
            # multiple topics can be created together
            self.admin.create_topics([new_topics])

            print(f"Topic: {topic} has been created")

        else:
            print(f"Topic: {topic} already exists")