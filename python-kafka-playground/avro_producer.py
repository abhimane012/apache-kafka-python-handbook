from admin import KafkaAdmin
from producer import KafkaProducerClient
from schema_registry_client import KafkaSchemaRegistryClient

from confluent_kafka.schema_registry.avro import AvroSerializer

from confluent_kafka.serialization import SerializationContext, MessageField

from uuid import uuid4


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
    ) -> None:

        # Initialize parent producer class
        super().__init__(bootstrap_servers, topic_name)

        self.schema_registry_client = schema_registry_client

        self.schema_definition = schema_definition

        # Create AVRO serializer
        self.avro_serializer = AvroSerializer(
            self.schema_registry_client, self.schema_definition
        )

    def send_message(self, message: dict) -> None:

        try:
            # Convert dictionary into AVRO bytes
            avro_message = self.avro_serializer(
                message, SerializationContext(self.topic_name, MessageField.VALUE)
            )

            # Send AVRO message to Kafka
            self.producer.produce(
                topic=self.topic_name,
                value=avro_message,
                key=str(uuid4()),
                headers={"correlation_id": str(uuid4())},
            )

            print(f"AVRO message sent: {avro_message}")

        except Exception as error:
            # Print error if sending fails
            print(error)

    def flush(self) -> None:
        # Ensure all pending messages are sent
        self.producer.flush()


if __name__ == "__main__":
    bootstrap_servers = "localhost:19092"

    topic_name = "test-topic"

    schema_registry_url = "http://localhost:18081"

    schema_type = "AVRO"

    # Create topic if not available
    kafka_admin = KafkaAdmin(bootstrap_servers)

    kafka_admin.create_topic(topic_name)

    # Read AVRO schema file
    with open("schema.avsc") as schema_file:
        schema_definition = schema_file.read()

    # Register schema
    schema_registry = KafkaSchemaRegistryClient(
        schema_registry_url, topic_name, schema_definition, schema_type
    )

    schema_registry.register_schema()

    # Create Kafka producer
    kafka_producer = KafkaAVROProducerClient(
        bootstrap_servers,
        topic_name,
        schema_registry.schema_registry_client,
        schema_definition,
    )

    try:
        # Continuously read user details
        while True:
            user_id = int(input("Enter user id: "))

            first_name = input("Enter first name: ")

            middle_name = input("Enter middle name: ")

            last_name = input("Enter last name: ")

            age = int(input("Enter age: "))

            # Create user object
            user = User(user_id, first_name, middle_name, last_name, age)

            # Send user data
            kafka_producer.send_message(user.get_dict())

    except KeyboardInterrupt:
        # Stop safely on Ctrl + C
        pass

    # Send remaining messages
    kafka_producer.flush()
