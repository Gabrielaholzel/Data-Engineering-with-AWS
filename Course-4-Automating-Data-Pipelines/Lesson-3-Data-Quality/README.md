# Data Quality
**Table of contents**
  * [What is Data Lineage?](#what-is-data-lineage)
      - [Definition](#definition)
      - [Why is Data Lineage important?](#why-is-data-lineage-important)
  * [Data Lineage in Airflow](#data-lineage-in-airflow)
  * [Tracing Inputs and Outputs](#tracing-inputs-and-outputs)
    + [Success of Individual Tasks](#success-of-individual-tasks)
  * [Data in Time Ranges](#data-in-time-ranges)
    + [Analyzing an Entire Dataset](#analyzing-an-entire-dataset)
      - [Schedules](#schedules)
          + [Why Schedules](#why-schedules)
    + [Selecting the time period](#selecting-the-time-period)
  * [Scheduling in Airflow](#scheduling-in-airflow)
    + [Partitioning](#partitioning)
        * [Schedule partitioning](#schedule-partitioning)
        * [Logical partitioning](#logical-partitioning)
        * [Size Partitioning](#size-partitioning)
    + [Why Data Partitioning?](#why-data-partitioning)
- [Pipeline Monitoring](#pipeline-monitoring)
  * [SLAs](#slas)
  * [Emails and Alerts](#emails-and-alerts)
  * [Metrics](#metrics)
  * [Logging](#logging)



## What is Data Lineage?

#### Definition

The data lineage of a dataset describes the discrete steps involved in the creation, movement, and calculation of that dataset.

#### Why is Data Lineage important?

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
