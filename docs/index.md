# Design Document

## Overview

Build a simple data pipeline that extract famous quotes, process it and save on storage.

- 🎯Goals: Deploy the pipeline into Databricks using different tools
- Non-Goals : Be a complex pipeline
- 🌟 Milestone: Follow best practices and principles
- Main Audience: Other interested engineers and I.
- Bonus : YAML file for CI/CD in GitHub Actions or Azure DevOps

## Requirements

| Requirement No | Requirement Summary                                      |
| -------------- | -------------------------------------------------------- |
| 1              | Use dbx                                                  |
| 2              | Use dba (Databricks Asset Bundles)                       |
| 3              | Apply Unit Testing on Python Code                        |
| 4              | Test Coverage be higher than 80%                         |
| 5              | Use Development Mix Mode ( Notebooks and Python Scripts) |
| 6              | Self document code using Docstrings                      |
| 7              | Documentation                                            |


## Design Considerations

### Data sources
It's an API hosted by [API Ninjas]([API Ninjas | Build Real Applications with Real Data (api-ninjas.com)](https://api-ninjas.com/)) and the user should sign up to get an API Key

### Data ingestion
Python code to request the quote and each request will get a new random quote. We can consider the  Data Volume small, being not a challenge in that use case.

### Data Storage
For the sake of simplicity will be stored in DBFS

### Data Processing
For further processing we will use [Delta Live Tables]([Configure pipeline settings for Delta Live Tables | Databricks on AWS](https://docs.databricks.com/en/delta-live-tables/settings.html))

- Autoloader will ingest incrementally to a `streaming` Bronze Table, adding some metadata information to track the batch and auditing purposes.
- Silver table we will hash some columns to uniquely identify a quote.
- Gold Tables for aggregation and report purposes.

### Data Consumption
No Data Consumers waiting in downstream tools

### Data Operations
The orchestration will be done by Databricks Workflows

### Data Governance
Out-of-Scope ❌

Data Security
Out-of-Scope ❌


## Tech Solution

### Workflow
- Draw the Architecture
- Data Assets

### Manage Metadata and Build Process:
- [Poetry](https://python-poetry.org/)
- [dbx](https://dbx.readthedocs.io/en/latest/)
- [Databricks Asset Bundles]([What are Databricks Asset Bundles? | Databricks on AWS](https://docs.databricks.com/en/dev-tools/bundles/index.html))  *check the repo here*

### Python Libraries:
 - pyspark
 - delta-spark
 - databricks-sdk
 - requests
#### Test
 - pytest
 - [chispa]([MrPowers/chispa: PySpark test helper methods with beautiful error messages (github.com)](https://github.com/MrPowers/chispa))
 - pytest-cov
 - pytest-mock

#### Linters
 - isort
 - black
#### Documentation
 - mkdocs
 - mkdocs-material



## References
>Alex Ott : [Applying software development & DevOps best practices to Delta Live Table pipelines | Databricks Blog](https://www.databricks.com/blog/applying-software-development-devops-best-practices-delta-live-table-pipelines)

>Matthew Powers: [Testing PySpark Code - MungingData](https://mungingdata.com/pyspark/testing-pytest-chispa/)

>[What is a Medallion Architecture? (databricks.com)](https://www.databricks.com/glossary/medallion-architecture)


> Eduardo Mendes : [(6) Documentado projetos com MkDocs - Live de Python #189 - YouTube](https://www.youtube.com/watch?v=GW6nAJ1NHUQ)