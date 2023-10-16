import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Column

def add_metadata_cols(df: DataFrame) -> DataFrame:
    """
    Adds metadata columns to a DataFrame.

    Args:
        df (DataFrame): The input DataFrame.

    Returns:
        DataFrame: A new DataFrame with additional metadata columns.

    Metadata Columns Added:
        - 'ingestion_datetime': Contains the file modification time from the metadata.
        - 'file_name': Contains the file name from the metadata.
    """
    df = df.withColumn("ingestion_datetime", F.col("_metadata.file_modification_time")) \
           .withColumn("file_name", F.col("_metadata.file_name"))

    return df


def drop_columns(df:DataFrame, cols_to_drop:list[str]) -> DataFrame:
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
        
    Returns:
        DataFrame: A new DataFrame with specified columns cast to the target data types.
    """
    keys = list(cols_to_cast.keys())

    for key in keys:
        df = df.withColumn(key, F.col(key).cast(cols_to_cast.get(key)))
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