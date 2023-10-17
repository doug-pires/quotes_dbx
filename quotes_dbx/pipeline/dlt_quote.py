# Databricks notebook source
import dlt
import pyspark.sql.functions as F
from pyspark.sql import Column, DataFrame

from quotes_dbx.common import add_metadata_cols
from quotes_dbx.provide_config import path_landing_quotes_dbx

# COMMAND ----------

options_quotes_df = {
    "format": "cloudFiles",
    "cloudFiles.format": "json",
    # "cloudFiles.schemaLocation": path_schema_autoloader,
    "cloudFiles.schemaEvolutionMode": "addNewColumns",
    "InferSchema": "true",
    "cloudFiles.inferColumnTypes": "true",
    "multiLine": "true",
}

# COMMAND ----------


@dlt.table(comment="Ingestion Quote data to Delta Table Bronze")
def bronze_table_quotes():
    df = (
        spark.readStream.format("cloudFiles")
        .options(**options_quotes_df)
        .load(path_landing_quotes_dbx)
    )
    df_quotes = df.transform(add_metadata_cols)
    return df_quotes
