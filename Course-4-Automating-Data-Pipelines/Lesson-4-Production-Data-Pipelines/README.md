# Production Data Pipelines
**Table of contents**
- [Airflow Contrib](#airflow-contrib)
  * [Airflow Provider Packages](#airflow-provider-packages)
- [Airflow Plugins](#airflow-plugins)
- [Best Practices for Data Pipeline Steps](#best-practices-for-data-pipeline-steps)
  * [Task Boundaries](#task-boundaries)
    + [Benefits of Task Boundaries](#benefits-of-task-boundaries)
- [Converting an Airflow 1 DAG](#converting-an-airflow-1-dag)
  * [Airflow 1 to Airflow 2](#airflow-1-to-airflow-2)
  * [Converting to Functional and Decorators](#converting-to-functional-and-decorators)
- [Pipeline Monitoring](#pipeline-monitoring)
  * [SLAs](#slas)
  * [Emails and Alerts](#emails-and-alerts)
  * [Metrics](#metrics)
  * [Logging](#logging)

## Airflow Contrib

  

### Airflow Provider Packages

  

Airflow boasts a dynamic open-source community that continually enhances and extends the platform's capabilities. Previously known as  [Airflow Contrib(opens in a new tab)](https://github.com/apache/airflow/tree/master/airflow/contrib), this community-driven repository has transformed, and its hooks and operators are now part of the  **Airflow Provider Packages**.

  

As an Airflow user, it is recommended that you explore  [Airflow Provider Packages(opens in a new tab)](https://github.com/apache/airflow/tree/main/airflow/providers)  before developing your plugins. This repository encompasses a variety of operators and hooks tailored for common data tools such as Apache Spark and Cassandra. Additionally, you'll find vendor-specific integrations for major cloud service providers like Amazon Web Services, Azure, and Google Cloud Platform.

  

If the desired functionality already exists but requires customization, this presents an excellent opportunity for open-source contributions. For further details on the Airflow Provider Packages, please refer to the  [Airflow documentation(opens in a new tab)](https://airflow.apache.org/docs/apache-airflow-providers/).

  

[Check out Airflow Provider Packages  
](https://github.com/apache/airflow/tree/main/airflow/providers)

## Airflow Plugins

Airflow was built with the intention of allowing its users to extend and customize its functionality through plugins. The most common types of user-created plugins for Airflow are Operators and Hooks. These plugins make DAGs reusable and simpler to maintain.

To create custom operator, follow the steps:

1.  Identify Operators that perform similar functions and can be consolidated
2.  Define a new Operator in the plugins folder
3.  Replace the original Operators with your new custom one, re-parameterize, and instantiate them.

[Here(opens in a new tab)](https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html)  is the Official Airflow Documentation for custom operators

## Best Practices for Data Pipeline Steps
### Task Boundaries

DAG tasks should be designed such that they are:

-   Atomic and have a single purpose
-   Maximize parallelism
-   Make failure states obvious

Every task in your dag should perform  **only one job.**

> “Write programs that do one thing and do it well.” - Ken Thompson’s Unix Philosophy

#### Benefits of Task Boundaries

-   Re-visitable: Task boundaries are useful for you if you revisit a pipeline you wrote after a 6 month absence. You'll have a much easier time understanding how it works and the lineage of the data if the boundaries between tasks are clear and well defined. This is true in the code itself, and within the Airflow UI.
-   Tasks that do just one thing are often more easily parallelized. This parallelization can offer a significant speedup in the execution of our DAGs.

## Converting an Airflow 1 DAG

### Airflow 1 to Airflow 2

By default most Airflow 1 DAGs just work in Airflow 2. There are some library changes, as some packages are deprecated in Airflow 2 that were previously supported. Features that will or will be deprecated include SubDAGs, and some Hooks like the AWSHook. Python syntax for Airflow 1  **will work**  for Airflow 2.

  

### Converting to Functional and Decorators

The main difference between Airflow 1 and Airflow 2 syntax is the functional paradigm, and the use of Decorators for Tasks and DAGs.

**Example:**

**Airflow 1**
```python


dag = DAG(
    'data_quality_legacy',
    start_date=pendulum.datetime(2018, 1, 1, 0, 0, 0, 0),
    end_date=pendulum.datetime(2018, 12, 1, 0, 0, 0, 0),
    schedule_interval='@monthly',
    max_active_runs=1
)

def load_trip_data_to_redshift(*args,* *kwargs):
    metastoreBackend = MetastoreBackend()
    aws_connection=metastoreBackend.get_connection("aws_credentials")
    redshift_hook = PostgresHook("redshift")
    execution_date = kwargs["execution_date"]
    sql_stmt = sql_statements.COPY_MONTHLY_TRIPS_SQL.format(
        aws_connection.login,
        aws_connection.password,
        year=execution_date.year,
        month=execution_date.month
    )
    redshift_hook.run(sql_stmt)

load_trips_task = PythonOperator(
    task_id='load_trips_from_s3_to_redshift',
    dag=dag,
    python_callable=load_trip_data_to_redshift,
    provide_context=True,
    sla=datetime.timedelta(hours=1)
)

. . .

create_trips_table >> load_trips_task
```





**Airflow 2**
```python
@dag(
    start_date=pendulum.datetime(2018, 1, 1, 0, 0, 0, 0),
    end_date=pendulum.datetime(2018, 12, 1, 0, 0, 0, 0),
    schedule_interval='@monthly',
    max_active_runs=1    
)
def data_quality():

    @task(sla=datetime.timedelta(hours=1))
    def load_trip_data_to_redshift(*args,* *kwargs):
        metastoreBackend = MetastoreBackend()
        aws_connection=metastoreBackend.get_connection("aws_credentials")
        redshift_hook = PostgresHook("redshift")
        execution_date = kwargs["execution_date"]
        sql_stmt = sql_statements.COPY_MONTHLY_TRIPS_SQL.format(
            aws_connection.login,
            aws_connection.password,
            year=execution_date.year,
            month=execution_date.month
        )
        redshift_hook.run(sql_stmt)

    load_trips_task = load_trip_data_to_redshift()

. . .

create_trips_table >> load_trips_task
```


## Pipeline Monitoring

Airflow can surface metrics and emails to help you stay on top of pipeline issues.

### SLAs

Airflow DAGs may optionally specify an SLA, or “Service Level Agreement”, which is defined as  **a time by which a DAG must complete.**  For time-sensitive applications these features are critical for developing trust amongst your pipeline customers and ensuring that data is delivered while it is still meaningful. Slipping SLAs can also be  **early indicators of performance problems**, or a need to scale up the size of your Airflow cluster

### Emails and Alerts

Airflow can be configured to send emails on DAG and task state changes. These state changes may include successes, failures, or retries. Failure emails can allow you to easily trigger alerts. It is common for alerting systems like PagerDuty to accept emails as a source of alerts. If a mission-critical data pipeline fails, you will need to know as soon as possible to get online and get it fixed.

### Metrics

Airflow comes out of the box with the ability to send system metrics using a metrics aggregator called statsd. Statsd can be coupled with metrics visualization tools like  [Grafana(opens in a new tab)](https://grafana.com/)  and monitoring tools like  [Prometheus(opens in a new tab)](https://prometheus.io/)  to provide you and your team high level insights into the overall performance of your DAGs, jobs, and tasks. These systems can be integrated into your alerting system, such as pagerduty, so that you can ensure problems are dealt with immediately. These Airflow system-level metrics allow you and your team to stay ahead of issues before they even occur by watching long-term trends.

### Logging

By default, Airflow logs to the local file system. You probably sifted through logs so far to see what was going on with the scheduler. Logs can be forwarded using standard logging tools like  [fluentd(opens in a new tab)](https://www.fluentd.org/).

See Airflow Logging and Monitoring architecture  [here(opens in a new tab)](https://airflow.apache.org/docs/apache-airflow/stable/logging-monitoring/logging-architecture.html).

