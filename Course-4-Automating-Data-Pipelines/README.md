# Course 4 - Automating Data Pipelines

## [Lesson 1 - Data Pipelines](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/tree/main/Course-4-Automating-Data-Pipelines/Lesson-1-Data-Pipelines)

- Define and describe a data pipeline and its usage.
- Explain the relationship between DAGs, S3, and Redshift within a given example.
- Employ tasks as instantiated operators.
- Organize task dependencies based on logic flow.
- Apply templating in codebase with kwargs parameter to set runtime variables.

## [Lesson 2 - Airflow and AWS](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/tree/main/Course-4-Automating-Data-Pipelines/Lesson-2-Airflow-and-AWS)

- Create Airflow Connection to AWS using AWS credentials.
- Create Postgres/Redshift Airflow Connections.
- Leverage hooks to use Connections in DAGs.
- Connect S3 to a Redshift DAG programmatically

## [Lesson 3 - Data Quality](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/tree/main/Course-4-Automating-Data-Pipelines/Lesson-3-Data-Quality)

- Utilize the logic flow of task dependencies to investigate potential errors within data lineage.
- Leverage Airflow catchup to backfill data.
- Extract data from a specific time range by employing the kwargs parameters.
- Create a task to ensure data quality within select tables.

## [Lesson 4 - Production Data Pipelines](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/tree/main/Course-4-Automating-Data-Pipelines/Lesson-4-Production-Data-Pipelines)

- Consolidate repeated code into operator plugins.
- Refactor a complex task into multiple tasks with separate SQL statements.
- Convert an Airflow 1 DAG into an Airflow 2 DAG.
- Construct a DAG and custom operator end-to-end
