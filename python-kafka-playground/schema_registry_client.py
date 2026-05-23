from confluent_kafka.schema_registry import SchemaRegistryClient, Schema

from confluent_kafka.schema_registry.error import SchemaRegistryError


class KafkaSchemaRegistryClient:
    def __init__(
        self,
        schema_registry_url: str,
        subject_name: str,
        schema_definition: str,
        schema_type: str,
    ) -> None:

        # Store schema registry URL
        self.schema_registry_url = schema_registry_url

        # Subject name used in schema registry
        self.subject_name = subject_name

        # Store schema content
        self.schema_definition = schema_definition

        # Store schema type
        # Example: AVRO, JSON, PROTOBUF
        self.schema_type = schema_type

        # Create schema registry client
        self.schema_registry_client = SchemaRegistryClient(
            {"url": self.schema_registry_url}
        )

    def schema_exists(self) -> bool:
        try:
            # Check whether schema already exists
            self.schema_registry_client.get_latest_version(self.subject_name)

            return True

        except SchemaRegistryError:
            return False

    def register_schema(self) -> None:

        # Register schema only if it does not exist
        if not self.schema_exists():
            try:
                # Create schema object
                schema = Schema(self.schema_definition, self.schema_type)

                # Register schema in schema registry
                self.schema_registry_client.register_schema(self.subject_name, schema)
                print("Schema Registerd Successfully")
            except SchemaRegistryError as error:
                # Print schema registration error
                print(error)
        else:
            print("Schema already registered")


if __name__ == "__main__":
    schema_registry_url = "http://localhost:18081"

    topic_name = "test-topic"

    schema_type = "AVRO"

    # Read AVRO schema from file
    with open("schema.avsc") as schema_file:
        schema_definition = schema_file.read()

    # Create schema registry client
    schema_registry = KafkaSchemaRegistryClient(
        schema_registry_url, topic_name, schema_definition, schema_type
    )

    # Register schema
    schema_registry.register_schema()
