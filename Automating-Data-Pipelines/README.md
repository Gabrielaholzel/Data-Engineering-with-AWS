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

