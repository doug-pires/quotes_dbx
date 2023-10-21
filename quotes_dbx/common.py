import pyspark.sql.functions as F
from pyspark.sql import Column, DataFrame

from quotes_dbx.config_logging import get_logger

logger = get_logger(__name__)


def add_metadata_cols(df: DataFrame) -> DataFrame:
    """
    Add metadata columns to a Spark DataFrame.
    Usually used in Databricks Autoloader
    https://docs.databricks.com/en/ingestion/file-metadata-column.html

    This function takes a Spark DataFrame and adds two columns, 'ingestion_datetime'
    and 'file_name', by extracting information from the '_metadata' column if it exists.

    Parameters:
    df (DataFrame): The input Spark DataFrame that may contain the '_metadata' column.

    Returns:
    DataFrame: A new Spark DataFrame with 'ingestion_datetime' and 'file_name' columns
    added if '_metadata' exists in the input DataFrame, or the original DataFrame if
    '_metadata' is not present.
    """
    df = df.withColumn(
        "file_modification_time", F.col("_metadata.file_modification_time")
    ).withColumn("file_name", F.col("_metadata.file_name"))

    return df



def drop_columns(df: DataFrame, cols_to_drop: list[str]) -> DataFrame:
    """
    Drops specified columns from a DataFrame.

    Args:
        df (DataFrame): The input DataFrame.
        cols_to_drop (list[str]): List of column names to be dropped.

    Returns:
        DataFrame: A new DataFrame with specified columns removed.
    """
    df = df.drop(*cols_to_drop)
    return df


def cast_cols(df: DataFrame, cols_to_cast: dict[str, str]) -> DataFrame:
    """
    Casts specified columns to the provided data types in a DataFrame.

    Args:
        df (DataFrame): The input DataFrame.
        cols_to_cast (dict[str, str]): A dictionary where keys are column names
            and values are the target data types for casting.
            Example: {"col_1": "int", "col_2": "boolean"}
    Returns:
        DataFrame: A new DataFrame with specified columns cast to the target data types.
    """
    cols = list(cols_to_cast.keys())

    for col in cols:
        type = cols_to_cast.get(col)
        df = df.withColumn(col, F.col(col).cast(type))
    return df


def group_by(df: DataFrame, col: str):
    """
    Group a DataFrame by a specified column and count the occurrences of each group.

    Parameters:
    df (DataFrame): The input DataFrame to be grouped.
    col (str): The name of the column by which to group the DataFrame.

    Returns:
    DataFrame: A new DataFrame with the groups and their corresponding counts.
    """
    df_grouped = df.groupBy(col).count()
    return df_grouped


if __name__ == "__main__":
    cols_to_be_casted = {"age": "int", "is_married": "boolean"}
    keys = list(cols_to_be_casted.keys())
    print(keys)
    for key in keys:
        type = cols_to_be_casted.get(key)
        col_name = f"{key}_casted"
        print(key, type, col_name)