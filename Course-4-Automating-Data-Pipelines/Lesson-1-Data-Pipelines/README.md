# Data Pipelines
**Table of contents**
- [Example](#example)
    + [Defining New Terms](#defining-new-terms)
      - [Extract Transform Load (ETL) and Extract Load Transform (ELT)](#extract-transform-load-etl-and-extract-load-transform-elt)
      - [What is S3?](#what-is-s3)
      - [What is Kafka?](#what-is-kafka)
      - [What is RedShift?](#what-is-redshift)
- [DAGs and Data Pipelines](#dags-and-data-pipelines)
  * [Definitions](#definitions)
- [Data Validation](#data-validation)
  * [What could go wrong?](#what-could-go-wrong)
  * [Data Validation in Action](#data-validation-in-action)
    + [In our bikesharing example, we could add the following validation steps:](#in-our-bikesharing-example-we-could-add-the-following-validation-steps)
    + [Why is this important?](#why-is-this-important)
     

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

## DAGs and Data Pipelines

### Definitions

-   **Directed Acyclic Graphs (DAGs):**  DAGs are a special subset of graphs in which the edges between nodes have a specific direction, and no cycles exist. When we say “no cycles exist” what we mean is the nodes can't create a path back to themselves.
-   **Nodes:**  A step in the data pipeline process.
-   **Edges:**  The dependencies or relationships other between nodes.

![Diagram of a Directed Acyclic Graph](https://video.udacity-data.com/topher/2019/February/5c5f5b00_capture/capture.png)



## Data Validation

Data Validation is the process of <u>ensuring that data is present, correct & meaningful</u>. Ensuring the quality of your data through automated validation checks is a critical step in building data pipelines at any organization.

### What could go wrong?

In our previous bikeshare example we loaded event data, analyzed it, and ranked our busiest locations to determine where to build additional capacity.

What would happen if the data was wrong?

### Data Validation in Action
#### In our bikesharing example, we could add the following validation steps:

After loading from S3 to Redshift:

-   Validate the number of rows in Redshift match the number of records in S3

Once location business analysis is complete:

-   Validate that all locations have a daily visit average greater than 0
-   Validate that the number of locations in our output table match the number of tables in the input table

#### Why is this important?

-   Data Pipelines provide a set of logical guidelines and a common set of terminology
-   The conceptual framework of data pipelines will help you better organize and execute everyday data engineering tasks
