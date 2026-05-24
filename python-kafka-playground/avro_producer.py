from admin import KafkaAdmin
from producer import KafkaProducerClient
from schema_registry_client import KafkaSchemaRegistryClient

from confluent_kafka.schema_registry.avro import AvroSerializer

from confluent_kafka.serialization import SerializationContext, MessageField

from uuid import uuid4


def delivery_callback(error, message) -> None:

    # Print error if delivery fails
    if error:
        print(f"Error while sending message to Kafka: {message.key()}")

    # Print message metadata
    print(
        f"Message delivered successfully "
        f"Topic={message.topic()}, "
        f"Key={message.key()}, "
        f"Offset={message.offset()}, "
        f"Partition={message.partition()}"
    )


class User:
    def __init__(
        self, user_id: int, first_name: str, middle_name: str, last_name: str, age: int
    ) -> None:

        # Store user details
        self.user_id = user_id
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.age = age

    def get_dict(self) -> dict:

        # Convert object into dictionary
        return dict(
            user_id=self.user_id,
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            age=self.age,
        )


class KafkaAVROProducerClient(KafkaProducerClient):
    def __init__(
        self,
        bootstrap_servers: str,
        topic_name: str,
        schema_registry_client,
        schema_definition: str,
        message_size: int | None = None,
        compression_type: str | None = None,
        batch_size: int | None = None,
        linger_ms: int | None = None,
    ) -> None:

        # Initialize base producer
        super().__init__(
            bootstrap_servers,
            topic_name,
            message_size,
            compression_type,
            batch_size,
            linger_ms,
        )

        # Store schema registry client
        self.schema_registry_client = schema_registry_client

        # Store schema definition
        self.schema_definition = schema_definition

        # Create AVRO serializer
        self.avro_serializer = AvroSerializer(
            self.schema_registry_client, self.schema_definition
        )

    def send_message(
        self, key: int | str | None = None, message_value: dict | None = None
    ) -> None:

        avro_message = None

        try:
            # Serialize only when
            # message data exists
            if message_value:
                avro_message = self.avro_serializer(
                    message_value,
                    SerializationContext(self.topic_name, MessageField.VALUE),
                )

                # Print message size
                print(f"Message size: {len(avro_message) / (1024 * 1024)} MB")

            # Send message
            # value=None creates
            # a Kafka tombstone event
            self.producer.produce(
                topic=self.topic_name,
                value=avro_message,
                key=str(key),
                headers={"correlation_id": str(uuid4())},
                callback=delivery_callback,
            )

            print("AVRO message sent successfully")

        except Exception as error:
            print(error, (len(avro_message) / (1024 * 1024) if avro_message else "N/A"))

    def flush(self) -> None:

        # Flush pending messages
        self.producer.flush()


if __name__ == "__main__":
    bootstrap_servers = "localhost:19092"

    topic_name = "test-topic"

    schema_registry_url = "http://localhost:18081"

    schema_type = "AVRO"

    # Create topic
    kafka_admin = KafkaAdmin(bootstrap_servers)

    kafka_admin.create_topic(topic_name, 2)

    # Read schema file
    with open("schema.avsc") as schema_file:
        schema_definition = schema_file.read()

    # Register schema
    kafka_schema_registry = KafkaSchemaRegistryClient(
        schema_registry_url, topic_name, schema_definition, schema_type
    )

    kafka_schema_registry.register_schema()

    # Create producer
    kafka_producer = KafkaAVROProducerClient(
        bootstrap_servers,
        topic_name,
        kafka_schema_registry.schema_registry_client,
        schema_definition,
        message_size=10 * 1024 * 1024,
        compression_type="snappy",
        batch_size=1_000_000,
        linger_ms=1000,
    )

    try:
        while True:
            choice = input("Do you want 'insert' or 'delete' (Tombstone): ")

            if choice == "insert":
                user_id = int(input("Enter user id: "))

                first_name = input("Enter first name: ")

                middle_name = input("Enter middle name: ")

                last_name = input("Enter last name: ")

                age = int(input("Enter age: "))

                user = User(user_id, first_name, middle_name, last_name, age)

                kafka_producer.send_message(key=user_id, message_value=user.get_dict())

            elif choice == "delete":
                user_id = int(input("Enter user id: "))

                # Send tombstone event
                kafka_producer.send_message(key=user_id)

    except KeyboardInterrupt:
        pass

    kafka_producer.flush()
