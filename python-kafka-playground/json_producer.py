from admin import KafkaAdmin
from producer import KafkaProducerClient
import json


class User:
    def __init__(
        self, first_name: str, middle_name: str, last_name: str, age: int
    ) -> None:

        # Store user details
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age

    def get_dict(self) -> dict:
        # Convert object into dictionary
        return dict(
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            age=self.age,
        )


class KafkaJSONProducerClient(KafkaProducerClient):
    def __init__(self, bootstrap_servers: str, topic_name: str) -> None:

        # Initialize parent producer class
        super().__init__(bootstrap_servers, topic_name)

        # Convert dictionary message
        # into JSON bytes
        self.json_serializer = lambda message: json.dumps(message).encode("utf-8")

    def send_message(self, message: dict) -> None:
        try:
            # Serialize dictionary into JSON
            json_message = self.json_serializer(message)

            # Send JSON message to Kafka
            self.producer.produce(self.topic_name, json_message)

        except Exception as error:
            # Print error if message sending fails
            print(error)

    def flush(self) -> None:
        # Ensure all buffered messages are sent
        self.producer.flush()


if __name__ == "__main__":
    bootstrap_servers = "localhost:19092"
    topic_name = "test-topic"

    # Create topic if it does not exist
    kafka_admin = KafkaAdmin(bootstrap_servers)
    kafka_admin.create_topic(topic_name)

    # Create producer client
    kafka_producer = KafkaJSONProducerClient(bootstrap_servers, topic_name)

    try:
        # Continuously read user details
        while True:
            first_name = input("Enter your first name: ")

            middle_name = input("Enter your middle name: ")

            last_name = input("Enter your last name: ")

            age = int(input("Enter your age: "))

            # Create user object
            user = User(first_name, middle_name, last_name, age)

            # Send user data to Kafka
            kafka_producer.send_message(user.get_dict())

    except KeyboardInterrupt:
        # Stop safely on Ctrl + C
        pass

    # Send remaining messages
    kafka_producer.flush()
