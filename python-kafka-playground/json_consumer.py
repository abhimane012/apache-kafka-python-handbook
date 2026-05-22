from consumer import KafkaConsumerClient
import json


class KafkaJSONConsumerClient(KafkaConsumerClient):
    def __init__(self, bootstrap_servers: str, group_id: str, topic_name: str) -> None:

        # Initialize parent consumer class
        super().__init__(bootstrap_servers, group_id, topic_name)

    def consume_messages(self) -> None:
        try:
            # Continuously poll for new messages
            while True:
                message = self.consumer.poll(1.0)

                # If no message is received, continue polling
                if not message:
                    continue

                # If Kafka returns an error
                if message.error():
                    print(f"Error while consuming message: {message.error()}")
                    continue

                # Convert bytes into UTF-8 string
                decoded_message = message.value().decode("utf-8")

                # Convert JSON string into dictionary
                json_message = json.loads(decoded_message)

                # Print decoded string message
                print(
                    f"Message Consumed: {decoded_message} Type: {type(decoded_message)}"
                )

                # Print JSON converted message
                print(
                    f"Message Consumed in JSON: "
                    f"{json_message} "
                    f"Type: {type(json_message)}"
                )

        except KeyboardInterrupt:
            # Stop consumer safely on Ctrl + C
            pass

        finally:
            # Close Kafka consumer connection
            self.consumer.close()


if __name__ == "__main__":
    bootstrap_servers = "localhost:19092"
    topic_name = "test-topic"
    group_id = "my-group-id"

    # Create consumer client
    kafka_consumer = KafkaJSONConsumerClient(bootstrap_servers, group_id, topic_name)

    # Subscribe to Kafka topic
    kafka_consumer.subscribe_topic()

    # Start consuming messages
    kafka_consumer.consume_messages()
