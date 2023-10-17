import pytest
from chispa import assert_df_equality
from pyspark.sql.types import StringType, StructField, StructType

from quotes_dbx.common import add_metadata_cols, cast_cols, drop_columns


def test_if_function_dropped_the_list_columns(spark_session, dummy_data):
    # Given the Data and Schema from Dummy Data
    # We create the Dataframe Persons
    # Having a list of columns to drop
    schema = dummy_data[0]
    data = dummy_data[1]
    df_persons = spark_session.createDataFrame(data=data, schema=schema)

    cols_to_be_removed = ["job", "city"]

    # When call the function drop call over a dataframe, the cols should be removed
    df_dropped_cols = df_persons.transform(
        drop_columns, cols_to_drop=cols_to_be_removed
    )
    # Then returns only the expected cols
    assert cols_to_be_removed not in df_dropped_cols.columns


def test_if_columns_provided_was_casted(spark_session, dummy_data):
    # Given the Data and Schema from Dummy Data
    schema = dummy_data[0]
    data = dummy_data[1]
    # We create the dataframe_persons_correct_schema with the CORRECT SCHEMA
    df_persons_correct_schema = spark_session.createDataFrame(data=data, schema=schema)
    # The dataframe_wrong_schema will have the WRONG SCHEMA with all STRINGTYPE columns.
    fields_wrong = [
        StructField("name", StringType(), nullable=True),
        StructField("age", StringType(), nullable=True),
        StructField("job", StringType(), nullable=True),
        StructField("country", StringType(), nullable=True),
        StructField("is_married", StringType(), nullable=True),
    ]
    schema_wrong = StructType(fields_wrong)
    df_wrong_schema = spark_session.createDataFrame(data=data, schema=schema_wrong)

    # Having a list of columns to cast. Age and IsMarried will  be casted to the correct type
    cols_to_be_casted = {"age": "int", "is_married": "boolean"}

    # When call the function drop call over a dataframe, the cols should be removed
    df_fixed = df_wrong_schema.transform(cast_cols, cols_to_cast=cols_to_be_casted)

    # Then returns only the expected cols comparing the Schema using Chispa
    assert_df_equality(df_persons_correct_schema, df_fixed)


@pytest.mark.parametrize(
    "expected_metadata_columns", ["file_name", "file_modification_time"]
)
def test_function_to_extract_metadata_from_dataframe(
    spark_session, dummy_metadata_data, expected_metadata_columns
):
    # Given the Data and Schema from Dummy Data containing Metadata
    schema = dummy_metadata_data[0]
    data = dummy_metadata_data[1]
    # We create the Dataframe Countries containing Metadata
    df_countries = spark_session.createDataFrame(data=data, schema=schema)

    # List of Metadata Columns I want to check
    # https://docs.databricks.com/en/ingestion/file-metadata-column.html

    # When call the function to add columns to extract the metadata
    df_with_metadata = df_countries.transform(add_metadata_cols)

    # Then assert the expected metadata cols were added
    assert expected_metadata_columns in df_with_metadata.columns
