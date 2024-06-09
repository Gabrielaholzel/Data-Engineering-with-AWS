# Apache Airflow

**Table of contents**
- [Components of Airflow](#components-of-airflow)
- [How Airflow Works](#how-airflow-works)
  * [Order of Operations For an Airflow DAG](#order-of-operations-for-an-airflow-dag)
- [DAGs, Operators and Tasks](#dags-operators-and-tasks)
  * [Operators](#operators)
  * [Use dag Decorators to Create a DAG](#use-dag-decorators-to-create-a-dag)
  * [Using Operators to Define Tasks](#using-operators-to-define-tasks)
  * [Using task Decorators to Define Tasks](#using-task-decorators-to-define-tasks)
  * [Schedules](#schedules)
- [Task Dependencies](#task-dependencies)
- [Airflow Hooks](#airflow-hooks)
  * [Connection via Airflow Hooks](#connection-via-airflow-hooks)

"Airflow is a platform to programmatically author, schedule and monitor workflows. Use airflow to author workflows as directed acyclic graphs (DAGs) of tasks. The airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed. When workflows are defined as code, they become more maintainable, versionable, testable, and collaborative."

If you'd like to learn more, start [here](https://airflow.apache.org/).


## Components of Airflow

![Airflow component diagram](https://video.udacity-data.com/topher/2022/August/62fea8ed_screen-shot-2022-08-18-at-3.01.37-pm/screen-shot-2022-08-18-at-3.01.37-pm.jpeg)

Airflow component diagram

-   **Scheduler**  orchestrates the execution of jobs on a trigger or schedule. The Scheduler chooses how to prioritize the running and execution of tasks within the system. You can learn more about the Scheduler from the official  [Apache Airflow documentation(opens in a new tab)](https://airflow.apache.org/scheduler.html).
-   **Work Queue**  is used by the scheduler in most Airflow installations to deliver tasks that need to be run to the  **Workers**.
-   **Worker**  processes execute the operations defined in each DAG. In most Airflow installations, workers pull from the  **work queue**  when it is ready to process a task. When the worker completes the execution of the task, it will attempt to process more work from the  **work queue**  until there is no further work remaining. When work in the queue arrives, the worker will begin to process it.
-   **Metastore Database**  saves credentials, connections, history, and configuration. The database, often referred to as the  _metadata database_, also stores the state of all tasks in the system. Airflow components interact with the database with the Python ORM,  [SQLAlchemy(opens in a new tab)](https://www.sqlalchemy.org/).
-   **Web Interface**  provides a control dashboard for users and maintainers. Throughout this course you will see how the web interface allows users to perform tasks such as stopping and starting DAGs, retrying failed tasks, configuring credentials, The web interface is built using the  [Flask web-development microframework(opens in a new tab)](http://flask.pocoo.org/).

## How Airflow Works

![Diagram of how Airflow works](https://video.udacity-data.com/topher/2019/February/5c5f8e1d_how-airflow-works/how-airflow-works.png)

### Order of Operations For an Airflow DAG

1.  The Airflow Scheduler starts DAGs based on time or external triggers.
2.  Once a DAG is started, the Scheduler looks at the steps within the DAG and determines which steps can run by looking at their dependencies.
3.  The Scheduler places runnable steps in the queue.
4.  Workers pick up those tasks and run them.
5.  Once the worker has finished running the step, the final status of the task is recorded and additional tasks are placed by the scheduler until all tasks are complete.
6.  Once all tasks have been completed, the DAG is complete.

## DAGs, Operators and Tasks

### Operators

Operators define the atomic steps of work that make up a DAG. Airflow comes with many Operators that can perform common operations. Here are a handful of common ones:

-   `PythonOperator`
-   `PostgresOperator`
-   `RedshiftToS3Operator`
-   `S3ToRedshiftOperator`
-   `BashOperator`
-   `SimpleHttpOperator`
-   `Sensor`

### Use dag Decorators to Create a DAG

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

  

### Using task Decorators to Define Tasks

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


## Task Dependencies

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


## Airflow Hooks

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
