from consumer import KafkaConsumerClient

from confluent_kafka.schema_registry.avro import AvroDeserializer

from schema_registry_client import KafkaSchemaRegistryClient

from confluent_kafka.serialization import SerializationContext, MessageField


class KafkaAVROConsumerClient(KafkaConsumerClient):
    def __init__(
        self,
        bootstrap_servers: str,
        group_id: str,
        topic_name: str,
        schema_registry_client,
        schema_definition: str,
    ) -> None:

        # Initialize parent consumer class
        super().__init__(bootstrap_servers, group_id, topic_name)

        # Store schema registry client
        self.schema_registry_client = schema_registry_client

        # Store schema content
        self.schema_definition = schema_definition

        # Create AVRO deserializer
        self.avro_deserializer = AvroDeserializer(
            self.schema_registry_client, self.schema_definition
        )

    def consume_messages(self) -> None:

        try:
            # Continuously poll for messages
            while True:
                message = self.consumer.poll(1.0)

                # Continue if no message received
                if not message:
                    continue

                # Print Kafka errors if any
                if message.error():
                    print(f"Error while consuming message: {message.error()}")

                    continue

                # Get raw byte message
                byte_message = message.value()

                print(f"Byte Message: {byte_message}, Type: {type(byte_message)}")

                # Convert AVRO bytes
                # back into Python dictionary
                deserialized_message = self.avro_deserializer(
                    byte_message,
                    SerializationContext(self.topic_name, MessageField.VALUE),
                )

                print(
                    f"Message Consumed "
                    f"in AVRO: "
                    f"{deserialized_message} "
                    f"Type: "
                    f"{type(deserialized_message)}"
                )

        except KeyboardInterrupt:
            # Stop consumer safely
            pass

        finally:
            # Close Kafka connection
            self.consumer.close()


if __name__ == "__main__":
    bootstrap_servers = "localhost:19092"

    topic_name = "test-topic"

    schema_registry_url = "http://localhost:18081"

    schema_type = "AVRO"

    group_id = "my-group-id"

    # Read schema file
    with open("schema.avsc") as schema_file:
        schema_definition = schema_file.read()

    # Create schema registry client
    kafka_schema_registry = KafkaSchemaRegistryClient(
        schema_registry_url, topic_name, schema_definition, schema_type
    )

    # Create consumer client
    kafka_consumer = KafkaAVROConsumerClient(
        bootstrap_servers,
        group_id,
        topic_name,
        kafka_schema_registry.schema_registry_client,
        schema_definition,
    )

    # Subscribe to Kafka topic
    kafka_consumer.subscribe_topic()

    # Start consuming messages
    kafka_consumer.consume_messages()
