# Databricks notebook source
import dlt
import pyspark.sql.functions as F
from pyspark.sql import Column, DataFrame

from quotes_dbx.common import add_metadata_cols,add_hash_col
from quotes_dbx.provide_config import path_landing_quotes_dbx,path_schema_autoloader

# COMMAND ----------

options_quotes_df = {
    "format": "cloudFiles",
    "cloudFiles.format": "json",
    "cloudFiles.schemaLocation": path_schema_autoloader,
    "cloudFiles.schemaEvolutionMode": "addNewColumns",
    "InferSchema": "true",
    # When Auto Loader infers the schema, a rescued data column is automatically added to your schema as _rescued_data. You can rename the column or include it in cases where you provide a schema by setting the option rescuedDataColumn.
    "cloudFiles.inferColumnTypes": "true",
    "multiline": "true",
}

# COMMAND ----------


@dlt.table(comment="Ingestion Quote data to Delta Table Bronze, adding metadata columns")
def bronze_table_quotes():
    df = (
        spark.readStream.format("cloudFiles")
        .options(**options_quotes_df)
        .load(path_landing_quotes_dbx)
    )
    df_quotes = df.transform(add_metadata_cols)
    return df_quotes

# COMMAND ----------

cols_to_hash = ["quote","author","category"]

# COMMAND ----------


@dlt.table(comment="Silver table, generating SK to uniquely identify unique quotes concanating author, quote and category")
def silver_quotes():
    df = ( dlt.read_stream("bronze_table_quotes") )
    df_quotes_add_hash_key = df.transform(add_hash_col,cols_to_hash)
    return df_quotes_add_hash_key
