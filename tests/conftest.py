import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    BooleanType,
    IntegerType,
    MapType,
    StringType,
    StructField,
    StructType,
)


@pytest.fixture(scope="session")
def spark_session() -> SparkSession:
    """
    PyTest fixture for creating a SparkSession.

    This fixture creates a SparkSession and automatically closes it at the end of the test session.
    """
    # Create a SparkSession
    spark = (
        SparkSession.builder.appName("pytest_spark_fixture")
        .master("local[1]")
        .getOrCreate()
    )

    # Set any necessary configuration options
    spark.conf.set("spark.sql.shuffle.partitions", "2")

    # Yield the SparkSession to the tests
    yield spark

    # Teardown - stop the SparkSession
    spark.stop()


@pytest.fixture(scope="session")
def dummy_data() -> list:
    fields = [
        StructField("name", StringType(), nullable=True),
        StructField("age", IntegerType(), nullable=True),
        StructField("job", StringType(), nullable=True),
        StructField("country", StringType(), nullable=True),
        StructField("is_married", BooleanType(), nullable=True),
    ]
    schema = StructType(fields)

    data = [
        ("Douglas", 31, "Engineer", "Brazil", True),
        ("Tifa", 25, "Doctor", "Germany", False),
        ("Marc", 88, "Retired", "Germany", True),
        ("Alberto", 35, "Mechanic", "Italy", True),
    ]

    return [schema, data]


@pytest.fixture(scope="session")
def dummy_metadata_data() -> list:
    # Returns list[ schema , data ]
    # Sample data for the "_metadata" column as a JSON string
    data = [
        {
            "country": "USA",
            "_metadata": {
                "file_path": "path/to/data",
                "file_name": "test.json",
                "file_modification_time": "2021-07-02 01:05:21",
            },
        },
        {
            "country": "Portugal",
            "_metadata": {
                "file_path": "path/to/other",
                "file_name": "example.json",
                "file_modification_time": "2021-12-20 02:06:21",
            },
        },
    ]
    # Define the schema for the DataFrame
    schema = StructType(
        [
            StructField("country", StringType(), nullable=True),
            StructField(
                "_metadata", MapType(StringType(), StringType()), nullable=True
            ),
        ]
    )

    return [schema, data]
