# COMMAND ----------

# MAGIC %sql
# MAGIC -- CREATE CATALOG IF NOT EXISTS catalog_quotes;
# MAGIC -- USE CATALOG catalog_quotes;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- CREATE SCHEMA IF NOT EXISTS quotes_dbx;

# COMMAND ----------

from quotes.provide_config import sql_cmd_create_catalog, sql_cmd_create_schema

# Create Catalog
spark.sql(sql_cmd_create_catalog)


# Create Schema
spark.sql(sql_cmd_create_schema)
