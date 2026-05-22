from confluent_kafka import Consumer


class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str, topic_name: str) -> None:
        # Kafka broker address
        self.bootstrap_servers = bootstrap_servers

        # Consumer group id (used for load balancing messages)
        self.group_id = group_id

        # Topic to consume messages from
        self.topic_name = topic_name

        # Kafka Consumer instance
        self.consumer = Consumer(
            {"bootstrap.servers": self.bootstrap_servers, "group.id": self.group_id}
        )

    def subscribe_topic(self) -> None:
        # Subscribe consumer to a Kafka topic
        # (uses instance topic_name in this simple design)
        self.consumer.subscribe([self.topic_name])

    def consume_messages(self) -> None:
        try:
            # Continuously poll for new messages
            while True:
                msg = self.consumer.poll(1.0)

                # If no message is received, continue polling
                if not msg:
                    continue

                # If Kafka returns an error, print it
                if msg.error():
                    print(f"Error while consuming message: {msg.error()}")
                    continue

                # Decode Kafka message bytes into a readable UTF-8 string and print it
                print(f"Message Consumed: {msg.value().decode('utf-8')}")

        except KeyboardInterrupt:
            # Stop consumer gracefully on Ctrl + C
            pass

        finally:
            # Close consumer connection properly
            self.consumer.close()


if __name__ == "__main__":
    bootstrap_servers = "localhost:19092"
    topic_name = "test-topic"
    group_id = "my-group-id"

    # Create consumer client
    kafka_consumer = KafkaConsumerClient(bootstrap_servers, group_id, topic_name)

    # Subscribe to topic
    kafka_consumer.subscribe_topic()

    # Start consuming messages
    kafka_consumer.consume_messages()
