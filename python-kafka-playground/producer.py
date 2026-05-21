from confluent_kafka import Producer
from admin import KafkaAdmin


class KafkaProducerClient:
    def __init__(self, bootstrap_servers: str, topic_name: str) -> None:
        # Kafka broker address
        self.bootstrap_servers = bootstrap_servers

        # Target topic where messages will be sent
        self.topic_name = topic_name

        # Kafka producer instance
        self.producer = Producer({"bootstrap.servers": self.bootstrap_servers})

    def send_message(self, message: str) -> None:
        try:
            # Send message to Kafka topic
            self.producer.produce(self.topic_name, message)

        except Exception as error:
            # Print error if message fails
            print(error)

    def flush(self) -> None:
        # Ensure all buffered messages are sent
        self.producer.flush()


if __name__ == "__main__":
    bootstrap_servers = "localhost:19092"
    topic_name = "test-topic"

    # Create Kafka admin and ensure topic exists
    kafka_admin = KafkaAdmin(bootstrap_servers)
    kafka_admin.create_topic(topic_name)

    # Create producer client
    kafka_producer = KafkaProducerClient(bootstrap_servers, topic_name)

    try:
        # Continuously read user input and send to Kafka
        while True:
            message = input("Enter your message: ")
            kafka_producer.send_message(message)

    except KeyboardInterrupt:
        # Stop safely on Ctrl + C
        pass

    # Flush remaining messages before exit
    kafka_producer.flush()
