from confluent_kafka import Producer
from admin import KafkaAdmin


class KafkaProducerClient:
    def __init__(
        self,
        bootstrap_servers: str,
        topic_name: str,
        message_size: int | None = None,
        compression_type: str | None = None,
        batch_size: int | None = None,
        linger_ms: int | None = None,
    ) -> None:

        # Kafka broker address
        self.bootstrap_servers = bootstrap_servers

        # Target topic for messages
        self.topic_name = topic_name

        # Producer configuration
        producer_config: dict = {"bootstrap.servers": self.bootstrap_servers}

        # Max message size
        if message_size:
            producer_config["message.max.bytes"] = message_size

        # Compression type (e.g., snappy, gzip)
        if compression_type:
            producer_config["compression.type"] = compression_type

        # Batch size in bytes
        if batch_size:
            producer_config["batch.size"] = batch_size

        # Linger time (delay before sending batch)
        if linger_ms:
            producer_config["linger.ms"] = linger_ms

        # Create Kafka producer
        self.producer = Producer(producer_config)

    def send_message(self, message: str) -> None:

        try:
            # Send message to Kafka topic
            self.producer.produce(self.topic_name, message)

        except Exception as error:
            # Print error + approximate message size in MB
            print(error, len(message) / (1024 * 1024))

    def flush(self) -> None:

        # Ensure all messages are delivered
        self.producer.flush()


if __name__ == "__main__":
    bootstrap_servers = "localhost:19092"

    topic_name = "test-topic"

    # Create topic if not exists
    kafka_admin = KafkaAdmin(bootstrap_servers)
    kafka_admin.create_topic(topic_name)

    # Create producer client
    kafka_producer = KafkaProducerClient(
        bootstrap_servers, topic_name, message_size=10 * 1024 * 1024
    )

    try:
        # Continuously read input
        while True:
            message = input("Enter your message: ")

            kafka_producer.send_message(message)

    except KeyboardInterrupt:
        # Stop safely
        pass

    # Flush remaining messages
    kafka_producer.flush()
