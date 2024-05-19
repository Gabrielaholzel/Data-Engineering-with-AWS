# Data Pipelines
A  **data pipeline**  describes, in code, a series of sequential data processing steps. Depending on the data requirements for each step, some steps may occur in parallel. Data pipelines also typically occur on a  **schedule**.  **Extract, transform and load (ETL)**, or  **extract, load, and transform (ELT)**, are common patterns found in data pipelines, but not strictly required. Some data pipelines perform only a subset of ETL or ELT.

Examples of data pipelines:

-   Personalized emails that are triggered after a data pipeline executed.
-   Companies commonly use data pipelines to orchestrate the analysis that determines pricing. For example, a rideshare app where you were offered real-time pricing.
-   a Bikeshare company, that wants to figure out where their busiest locations are. They might use this data to determine where to build additional locations, or simply to add more bikes. A data pipeline to accomplish this task would likely first load application event data from a source such as  **S3**  or  **Kafka**. Second, we might take that data and then load it into an analytic warehouse such as RedShift. Then third, perform data transformations that identify high-traffic bike docks.

## Example

Pretend we work at a bikeshare company and want to email customers who don’t complete a purchase.

A data pipeline to accomplish this task would likely:

-   Load application event data from a source such as  **S3**  or  **Kafka**
-   Load the data into an analytic warehouse such as  **RedShift**
-   Perform data transformations that identify high-traffic bike docks so the business can determine where to build additional locations

![Graph of an example pipeline](https://video.udacity-data.com/topher/2021/September/615152f9_lesson-1-/lesson-1-.png)


#### Defining New Terms

##### Extract Transform Load (ETL) and Extract Load Transform (ELT):

"ETL is normally a continuous, ongoing process with a well-defined workflow. ETL first extracts data from homogeneous or heterogeneous data sources. Then, data is cleansed, enriched, transformed, and stored either back in the lake or in a data warehouse.

"ELT (Extract, Load, Transform) is a variant of ETL wherein the extracted data is first loaded into the target system. Transformations are performed after the data is loaded into the data warehouse. ELT typically works well when the target system is powerful enough to handle transformations. Analytical databases like Amazon Redshift and Google BigQuery."  _Source:_  [Xplenty.com(opens in a new tab)](https://www.xplenty.com/blog/etl-vs-elt/)

##### What is S3?

"Amazon S3 has a simple web services interface that you can use to store and retrieve any amount of data, at any time, from anywhere on the web. It gives any developer access to the same highly scalable, reliable, fast, inexpensive data storage infrastructure that Amazon uses to run its own global network of web sites."

_Source:_  [Amazon Web Services Documentation(opens in a new tab)](https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

If you want to learn more, start  [here(opens in a new tab)](https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html).

##### What is Kafka?

"Apache Kafka is an  **open-source stream-processing software platform**  developed by Linkedin and donated to the Apache Software Foundation, written in Scala and Java. The project aims to provide a unified, high-throughput, low-latency platform for handling real-time data feeds. Its storage layer is essentially a massively scalable pub/sub message queue designed as a distributed transaction log, making it highly valuable for enterprise infrastructures to process streaming data."  _Source:_  _Wikipedia_.

If you want to learn more, start  [here(opens in a new tab)](https://kafka.apache.org/intro).

##### What is RedShift?

"Amazon Redshift is a fully managed, petabyte-scale data warehouse service in the cloud. You can start with just a few hundred gigabytes of data and scale to a petabyte or more... The first step to create a data warehouse is to launch a set of nodes, called an Amazon Redshift cluster. After you provision your cluster, you can upload your data set and then perform data analysis queries. Regardless of the size of the data set, Amazon Redshift offers fast query performance using the same SQL-based tools and business intelligence applications that you use today.

If you want to learn more, start  [here(opens in a new tab)](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html).

So in other words, S3 is an example of the final data store where data might be loaded (e.g. ETL). While Redshift is an example of a data warehouse product, provided specifically by Amazon.

# DAGs and Data Pipelines

#### Definitions

-   **Directed Acyclic Graphs (DAGs):**  DAGs are a special subset of graphs in which the edges between nodes have a specific direction, and no cycles exist. When we say “no cycles exist” what we mean is the nodes can't create a path back to themselves.
-   **Nodes:**  A step in the data pipeline process.
-   **Edges:**  The dependencies or relationships other between nodes.

![Diagram of a Directed Acyclic Graph](https://video.udacity-data.com/topher/2019/February/5c5f5b00_capture/capture.png)



# Data Validation

Data Validation is the process of <u>ensuring that data is present, correct & meaningful</u>. Ensuring the quality of your data through automated validation checks is a critical step in building data pipelines at any organization.

## What could go wrong?

In our previous bikeshare example we loaded event data, analyzed it, and ranked our busiest locations to determine where to build additional capacity.

What would happen if the data was wrong?

## Data Validation in Action
#### In our bikesharing example, we could add the following validation steps:

After loading from S3 to Redshift:

-   Validate the number of rows in Redshift match the number of records in S3

Once location business analysis is complete:

-   Validate that all locations have a daily visit average greater than 0
-   Validate that the number of locations in our output table match the number of tables in the input table

## Why is this important?

-   Data Pipelines provide a set of logical guidelines and a common set of terminology
-   The conceptual framework of data pipelines will help you better organize and execute everyday data engineering tasks


# Apache Airflow

"Airflow is a platform to programmatically author, schedule and monitor workflows. Use airflow to author workflows as directed acyclic graphs (DAGs) of tasks. The airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed. When workflows are defined as code, they become more maintainable, versionable, testable, and collaborative."

If you'd like to learn more, start [here](https://airflow.apache.org/).


# How Airflow Works

### 

Components of Airflow

![Airflow component diagram](https://video.udacity-data.com/topher/2022/August/62fea8ed_screen-shot-2022-08-18-at-3.01.37-pm/screen-shot-2022-08-18-at-3.01.37-pm.jpeg)

Airflow component diagram

-   **Scheduler**  orchestrates the execution of jobs on a trigger or schedule. The Scheduler chooses how to prioritize the running and execution of tasks within the system. You can learn more about the Scheduler from the official  [Apache Airflow documentation(opens in a new tab)](https://airflow.apache.org/scheduler.html).
-   **Work Queue**  is used by the scheduler in most Airflow installations to deliver tasks that need to be run to the  **Workers**.
-   **Worker**  processes execute the operations defined in each DAG. In most Airflow installations, workers pull from the  **work queue**  when it is ready to process a task. When the worker completes the execution of the task, it will attempt to process more work from the  **work queue**  until there is no further work remaining. When work in the queue arrives, the worker will begin to process it.
-   **Metastore Database**  saves credentials, connections, history, and configuration. The database, often referred to as the  _metadata database_, also stores the state of all tasks in the system. Airflow components interact with the database with the Python ORM,  [SQLAlchemy(opens in a new tab)](https://www.sqlalchemy.org/).
-   **Web Interface**  provides a control dashboard for users and maintainers. Throughout this course you will see how the web interface allows users to perform tasks such as stopping and starting DAGs, retrying failed tasks, configuring credentials, The web interface is built using the  [Flask web-development microframework(opens in a new tab)](http://flask.pocoo.org/).

### How Airflow Works

![Diagram of how Airflow works](https://video.udacity-data.com/topher/2019/February/5c5f8e1d_how-airflow-works/how-airflow-works.png)

### Order of Operations For an Airflow DAG

1.  The Airflow Scheduler starts DAGs based on time or external triggers.
2.  Once a DAG is started, the Scheduler looks at the steps within the DAG and determines which steps can run by looking at their dependencies.
3.  The Scheduler places runnable steps in the queue.
4.  Workers pick up those tasks and run them.
5.  Once the worker has finished running the step, the final status of the task is recorded and additional tasks are placed by the scheduler until all tasks are complete.
6.  Once all tasks have been completed, the DAG is complete.

# DAGs, Operators and Tasks

### Operators

Operators define the atomic steps of work that make up a DAG. Airflow comes with many Operators that can perform common operations. Here are a handful of common ones:

-   `PythonOperator`
-   `PostgresOperator`
-   `RedshiftToS3Operator`
-   `S3ToRedshiftOperator`
-   `BashOperator`
-   `SimpleHttpOperator`
-   `Sensor`

### Use  `@dag`  Decorators to Create a DAG

A  **DAG Decorator**  is an annotation used to mark a function as the definition of a DAG. You can set attributes about the DAG, like: name, description, start date, and interval. The function itself marks the beginning of the definition of the DAG.

```python
import pendulum 
import logging from airflow.decorators 
import dag 
@dag(description='Analyzes Divvy Bikeshare Data',
	start_date=pendulum.now(), 
	schedule_interval='@daily')  
	def  divvy_dag():
```

  

### Using Operators to Define Tasks

**Operators**  define the atomic steps of work that make up a DAG. Instantiated operators are referred to as  **Tasks**.

```python
from airflow import DAG 
from airflow.operators.python_operator import PythonOperator

def  hello_world():
	print(“Hello World”)  

divvy_dag =  DAG(...)
task =  PythonOperator(
	task_id=’hello_world’,
	python_callable=hello_world,
	dag=divvy_dag)
```

  

### Using  `@task`  Decorators to Define Tasks

A  **Task Decorator**  is an annotation used to mark a function as a  **custom operator**, that generates a task.

 ```python
 @task()
 def hello_world_task():
	 logging.info("Hello World")
```

  

### Schedules

**Schedules**  are optional, and may be defined with cron strings or Airflow Presets. Airflow provides the following presets:

-   `@once`  - Run a DAG once and then never again
-   `@hourly`  - Run the DAG every hour
-   `@daily`  - Run the DAG every day
-   `@weekly`  - Run the DAG every week
-   `@monthly`  - Run the DAG every month
-   `@yearly`- Run the DAG every year
-   `None`  - Only run the DAG when the user initiates it

**Start Date:**  If your start date is in the past, Airflow will run your DAG as many times as there are schedule intervals between that start date and the current date.

**End Date:**  Unless you specify an optional end date, Airflow will continue to run your DAGs until you disable or delete the DAG.


# Task Dependencies

In Airflow DAGs:

-   Nodes = Tasks
-   Edges = Ordering and dependencies between tasks

Task dependencies can be described programmatically in Airflow using  `>>`  and  `<<`

-   a  `>>`  b means a comes before b
-   a  `<<`  b means a comes after b

 ```python
hello_world_task = PythonOperator(task_id=’hello_world’, ...)
goodbye_world_task = PythonOperator(task_id=’goodbye_world’, ...)  
...
	# Use >> to denote that goodbye_world_task depends on hello_world_task
hello_world_task >> goodbye_world_task
```

Tasks dependencies can also be set with “set_downstream” and “set_upstream”

-   `a.set_downstream(b)`  means a comes before b
-   `a.set_upstream(b)`  means a comes after b

 ```python
 hello_world_task = PythonOperator(task_id=’hello_world’, ...)
 goodbye_world_task = PythonOperator(task_id=’goodbye_world’, ...)
 ...
 hello_world_task.set_downstream(goodbye_world_task)
```


# Airflow Hooks

### Connection via Airflow Hooks

Connections can be accessed in code via hooks. Hooks provide a reusable interface to external systems and databases. With hooks, you don’t have to worry about how and where to store these connection strings and secrets in your code.

 ```python
 from airflow import DAG 
 from airflow.hooks.postgres_hook import PostgresHook 
 from airflow.operators.python_operator import PythonOperator 

def  load():
	# Create a PostgresHook option using the `demo` connection  
	db_hook = PostgresHook(‘demo’)  
	df = db_hook.get_pandas_df('SELECT * FROM rides')
	print(f'Successfully used PostgresHook to return {len(df)} records')

load_task = PythonOperator(task_id=’load’, 
	python_callable=hello_world,...)
```

Airflow comes with many Hooks that can integrate with common systems. Here are a few common ones:

-   `HttpHook`
-   `PostgresHook`  (works with RedShift)
-   `MySqlHook`
-   `SlackHook`
-   `PrestoHook`

# Data Quality

## What is Data Lineage?

##### Definition

The data lineage of a dataset describes the discrete steps involved in the creation, movement, and calculation of that dataset.

##### Why is Data Lineage important?

1.  **Instilling Confidence:**  Being able to describe the data lineage of a particular dataset or analysis will build confidence in data consumers (engineers, analysts, data scientists, etc.) that our data pipeline is creating meaningful results using the correct datasets. If the data lineage is unclear, its less likely that the data consumers will trust or use the data.
2.  **Defining Metrics:**  Another major benefit of surfacing data lineage is that it allows everyone in the organization to agree on the definition of how a particular metric is calculated.
3.  **Debugging:**  Data lineage helps data engineers track down the root of errors when they occur. If each step of the data movement and transformation process is well described, it's easy to find problems when they occur.

In general, data lineage has important implications for a business. Each department or business unit's success is tied to data and to the flow of data between departments. For e.g., sales departments rely on data to make sales forecasts, while at the same time the finance department would need to track sales and revenue. Each of these departments and roles depend on data, and knowing where to find the data. Data flow and data lineage tools enable data engineers and architects to track the flow of this large web of data.


## Data Lineage in Airflow

Task dependencies can be used to reflect data lineage. 

This is an example of using data lineage to address data quality problems.

`create_table >> load_from_s3_to_redshift >> calculate_location_traffic`

## Tracing Inputs and Outputs

In our bikeshare example, we can trace the input and output data at every step of the way:

-   A csv is loaded from S3 to Redshift
-   The trips table in Redshift is analyzed to produce the station_traffic table

![S3 to Redshift, CSV file, Redshift Analysis, and sample data](https://video.udacity-data.com/topher/2022/September/63113ae2_screen-shot-2022-09-01-at-4.04.45-pm/screen-shot-2022-09-01-at-4.04.45-pm.jpeg)

### Success of Individual Tasks

In Airflow, the graph view of a DAG can let us see the success or failures of individual tasks.

The location_traffic task in the DAG run below has failed.

![Green create table block, Green copy to redshift block, red location traffic block](https://video.udacity-data.com/topher/2022/September/63113c55_screen-shot-2022-09-01-at-4.12.05-pm/screen-shot-2022-09-01-at-4.12.05-pm.jpeg)

Airflow DAGs are a natural representation for the movement & transformation of data.

![Green create table block, Green copy to redshift block, Green location traffic block](https://video.udacity-data.com/topher/2022/September/63113cd6_screen-shot-2022-09-01-at-4.14.09-pm/screen-shot-2022-09-01-at-4.14.09-pm.jpeg)

Airflow keeps a record of historical DAG and task executions, but it does not store the code from those historical runs. Whatever the latest code is in your DAG definition is what Airflow will render for you in the browser.


## Data in Time Ranges

Pipeline schedules can be used to enhance our analyses by allowing us to make assumptions about the scope of the data we’re analyzing. What do we mean when we say the scope of the data?

When a data pipeline is designed with a schedule in mind, we can use the execution time of the pipeline run to only analyze data from the time period since this data pipeline last ran.

**In a naive analysis, with no scope, we would analyze all of the data at all times.**

  

### Analyzing an Entire Dataset

Earlier we created an Airflow DAG that built a station_traffic table containing an analysis of all the 2018 data available for our bikeshare company. The scope of this data was the entire dataset.

![Redshift Analysis block, encompasses data from entire year](https://video.udacity-data.com/topher/2022/September/63113f47_screen-shot-2022-09-01-at-4.22.03-pm/screen-shot-2022-09-01-at-4.22.03-pm.jpeg)

That works fine for data in the past. However, if you are running  **daily loads**  of  **growing datasets**, a different approach is required.

A better approach would be to scope the analysis by scheduling a smaller time period.

![Redshift Analysis block scoped to a single month](https://video.udacity-data.com/topher/2022/September/631140a9_screen-shot-2022-09-01-at-4.30.30-pm/screen-shot-2022-09-01-at-4.30.30-pm.jpeg)

#### Schedules

Pipelines are often driven by schedules which determine what data should be analyzed and when.

###### Why Schedules

-   Pipeline schedules can reduce the amount of data that needs to be processed in a given run. It helps scope the job to only run the data for the time period since the data pipeline last ran. In a naive analysis, with no scope, we would analyze all of the data at all times.
-   Using schedules to select only data relevant to the time period of the given pipeline execution can help improve the quality and accuracy of the analyses performed by our pipeline.
-   Running pipelines on a schedule will decrease the time it takes the pipeline to run.
-   An analysis of larger scope can leverage already-completed work. For. e.g., if the aggregates for all months prior to now have already been done by a scheduled job, then we only need to perform the aggregation for the current month and add it to the existing totals.

### Selecting the time period

Determining the appropriate time period for a schedule is based on a number of factors which you need to consider as the pipeline designer.

1.  **What is the size of data, on average, for a time period?**  If an entire years worth of data is only a few kb or mb, then perhaps its fine to load the entire dataset. If an hours worth of data is hundreds of mb or even in the gbs then likely you will need to schedule your pipeline more frequently.
2.  **How frequently is data arriving, and how often does the analysis need to be performed?**  If our bikeshare company needs trip data every hour, that will be a driving factor in determining the schedule. Alternatively, if we have to load hundreds of thousands of tiny records, even if they don't add up to much in terms of mb or gb, the file access alone will slow down our analysis and we’ll likely want to run it more often.
3.  **What's the frequency on related datasets?**  A good rule of thumb is that the frequency of a pipeline’s schedule should be determined by the dataset in our pipeline which requires the most frequent analysis. This isn’t universally the case, but it's a good starting assumption. For example, if our trips data is updating every hour, but our bikeshare station table only updates once a quarter, we’ll probably want to run our trip analysis every hour, and not once a quarter.


## Scheduling in Airflow

Airflow will  **catchup**  by creating a DAG run for every period defined by the schedule_interval between the start_date and now.

![DAG historical run intervals](https://video.udacity-data.com/topher/2022/September/6311431e_screen-shot-2022-09-01-at-4.40.49-pm/screen-shot-2022-09-01-at-4.40.49-pm.jpeg)

**Catchup**

Airflow uses the schedule interval to create historical DAG runs and catchup data.

Whenever the start date of a DAG is in the past, and the time difference between the start date and now includes more than one schedule intervals, Airflow will automatically schedule and execute a DAG run to satisfy each one of those intervals.  **Catchup**  is enabled by default. See the sample code below to disable catchup at a DAG level.

**Start Date**

Airflow will begin running pipelines on the date in the  `start_date`  parameter . This is the date when a scheduled DAG will start executing on its own. In the sample code below, the DAG will be scheduled to run daily beginning  **immediately**.

`@dag(   # schedule to run daily   # once it is enabled in Airflow  schedule_interval='@daily',  start_date=pendulum.now(),  catchup=False  )`

**End Date**

Airflow pipelines can optionally have end dates. You can use an  `end_date`  parameter to let Airflow know the date it should stop running a scheduled pipeline. End_dates can also be useful when you want to perform an overhaul or redesign of an existing pipeline. Update the old pipeline with an  `end_date`  and then have the new pipeline start on the end date of the old pipeline.

  

In the sample code below, the DAG will be scheduled to run daily, beginning August 1st 2022, and end running September 1st 2022.

```python
@dag(
    start_date=pendulum.datetime(2022, 8, 1, 0, 0, 0, 0),
    end_date=pendulum.datetime(2022, 9, 1, 0, 0, 0, 0),
    schedule_interval='@daily',
    max_active_runs=1    
)
```


### Partitioning

##### Schedule partitioning

Not only are schedules great for reducing the amount of data our pipelines have to process, but they also help us guarantee that we can meet timing guarantees that our data consumers may need.

##### Logical partitioning

Conceptually related data can be partitioned into discrete segments and processed separately. This process of separating data based on its conceptual relationship is called logical partitioning. With logical partitioning, unrelated things belong in separate steps. Consider your dependencies and separate processing around those boundaries.

Also worth mentioning, the data  _location_  is another form of logical partitioning. For example, if our data is stored in a key-value store like Amazon's S3 in a format such as:  `s3://<bucket>/<year>/<month>/<day>`  we could say that our date is logically partitioned by time.

##### Size Partitioning

Size partitioning separates data for processing based on desired or required storage limits. This essentially sets the amount of data included in a data pipeline run. Size partitioning is critical to understand when working with large datasets, especially with Airflow.


### Why Data Partitioning?

Pipelines designed to work with partitioned data fail more gracefully. Smaller datasets, smaller time periods, and related concepts are easier to debug than big datasets, large time periods, and unrelated concepts. Partitioning makes debugging and rerunning failed tasks much simpler. It also enables easier redos of work, reducing cost and time.

Another great thing about Airflow is that if your data is partitioned appropriately, your tasks will naturally have fewer dependencies on each other. Because of this, Airflow will be able to parallelize execution of your DAGs to produce your results even faster.



# Pipeline Monitoring

Airflow can surface metrics and emails to help you stay on top of pipeline issues.

#### SLAs

Airflow DAGs may optionally specify an SLA, or “Service Level Agreement”, which is defined as  **a time by which a DAG must complete.**  For time-sensitive applications these features are critical for developing trust amongst your pipeline customers and ensuring that data is delivered while it is still meaningful. Slipping SLAs can also be  **early indicators of performance problems**, or a need to scale up the size of your Airflow cluster

#### Emails and Alerts

Airflow can be configured to send emails on DAG and task state changes. These state changes may include successes, failures, or retries. Failure emails can allow you to easily trigger alerts. It is common for alerting systems like PagerDuty to accept emails as a source of alerts. If a mission-critical data pipeline fails, you will need to know as soon as possible to get online and get it fixed.

#### Metrics

Airflow comes out of the box with the ability to send system metrics using a metrics aggregator called statsd. Statsd can be coupled with metrics visualization tools like  [Grafana(opens in a new tab)](https://grafana.com/)  and monitoring tools like  [Prometheus(opens in a new tab)](https://prometheus.io/)  to provide you and your team high level insights into the overall performance of your DAGs, jobs, and tasks. These systems can be integrated into your alerting system, such as pagerduty, so that you can ensure problems are dealt with immediately. These Airflow system-level metrics allow you and your team to stay ahead of issues before they even occur by watching long-term trends.

#### Logging

By default, Airflow logs to the local file system. You probably sifted through logs so far to see what was going on with the scheduler. Logs can be forwarded using standard logging tools like  [fluentd(opens in a new tab)](https://www.fluentd.org/).

### See Airflow Logging and Monitoring architecture  [here(opens in a new tab)](https://airflow.apache.org/docs/apache-airflow/stable/logging-monitoring/logging-architecture.html).
