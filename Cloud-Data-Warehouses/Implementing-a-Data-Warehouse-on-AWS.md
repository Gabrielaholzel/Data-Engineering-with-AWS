# Implementing a Data Warehouse on AWS

## Amazon Redshift

Redshift is a **column-oriented RDBMS** that is best suited of online analytical processing (OLAP) workloads. A key difference is the way queries are executed. Most relational databases will execute multiple queries in parallel if they have access to many cores or servers. If you have an RDBMS database cluster, many queries can run at the same time, but each query runs on only one CPU. If there're a lot of concurrent users running queries, they can be scheduled on CPUs. This turns out to be appropriate for OLTP applications because there are a lot of concurrent users, each running small queries, like an update or retrieving a few rows. 

![Redshift](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/20b1a0841fc57831d8e54aa087595d563376ef86/Images/amazon-redshift.jpg)

When you're building a data warehouse solution though, and dealing with large amounts of data, you'll need a database capable of **massive parallel processing (MPP)**. MPP databases like Amazon Redshift parallelise the execution of a single query on multiple CPUs and multiple machines. 

Tables in MPP databases are partitioned into smaller partitions and distributed across CPUs and each CPU also has its own associated storage. One query can process a whole table in parallel and each CPU is processing only one partition of the data. 

![Queries in Redshift](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/20b1a0841fc57831d8e54aa087595d563376ef86/Images/queries-in-Redshift.jpg)


Redshift is a cluster of machines composed of one leader node and one or more compute nodes. You can run a cluster with a single node, though. The leader node interacts with the outside world. Client applications talk to the leader node using protocols like JDBC or ODBC. To them, it's like any other normal database. 

However, under the hood, the leader node commands a number of compute nodes. The leader node coordinates the work of these compute nodes. It handles external communication and optimises query execution. 

Each compute node has its own CPU, memory and disk, and you can configure how powerful the cluster will be, as well as configuring whether you want to scale up or scale out. **Scaling up** means adding more nodes and **scaling out** means fewer but larger nodes. Each compute node is logically divided into a number of slices. For simplicity, you can think of a slice as a CPU with many disks dedicated to its work. A cluster with n slices can process n partitions of a table simultaneously. <u>The sum of all slices across all compute nodes is the unit of parallelisation, i.e. the total number of slices in a cluster is equal to the sum of all slices on the cluster</u>. 

![Redshift Cluster Architecture](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/9d49a22479ac4a8fb951de27754cfc5ad13d78be/Images/redshift-architecture.jpg)

If you have a Redshift cluster with a dc1 large EC2 instance which has two CPUs, it'll have two slices. It has 15 gigabytes of RAM and a 60 gigabyte solid-state drive. You can have from 1 to 32 in a cluster, giving you a total capacity of around five terabytes. 

You can also choose storage optimised nodes. These nodes are not as fast or powerful in terms of CPU, but they are larger in capacity. One of these has 36 CPUs. You can configure up to 128, giving you a capacity around two petabytes. However, these instances are rather expensive. For example, a dc2 large instance costs $0.25 per hour. If you use four of these in a cluster, you'll pay $1 per hour, so it's very important to stop or delete these resources if you're not using them. 

![Redshift Node Types](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/9d49a22479ac4a8fb951de27754cfc5ad13d78be/Images/redshift-node-types.jpg)


### Amazon Redshift Architecture

**LeaderNode:**

-   Coordinates compute nodes
-   Handles external communication
-   Optimizes query execution

**Compute Nodes:**

-   Each with own CPU, memory, and disk (determined by the node type)
-   Scale up: get more powerful nodes
-   Scale out: get more nodes

**Node Slices:**

-   Each compute node is logically divided into a number of slices
-   A cluster with n slices can process n partitions of tables simultaneously



## Ingesting Data at Scale

We can use SQL queries to select data out of a database. But what do we do if we want to copy the results to another table on a totally different database server like Redshift? We want to move the data from here to there. 

One way to approach SQL to SQL ETL is to put an ETL server between the source database and the destination data warehouse. We can use SQL statements to get the data. The data is written to CSVs in the local storage or network-attached storage of that ETL server, and you would insert or copy the data to the data warehouse.

![Data Warehouse ETL](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/c484f32f02ab4808d5908823c4777890278c382d/Images/data-warehouse-ETL.jpg)

On the AWS platform, we could use EC2 instances as ETL servers. But there is an even better way to take advantage of the AWS platform. <u> S3 distributed storage buckets can be used as a staging area for data to be loaded into Redshift</u>. Most of the products on the AWS platform, especially the managed service products, are able to communicate with S3 storage. You can extract data from multiple data sources within ETL server into S3 as a staging area, using SQL to transform it and load it into Redshift.

![Redshift SQL to SQL ETL](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/c484f32f02ab4808d5908823c4777890278c382d/Images/redshift-sql-to-sql-ETL.jpg)

Let's review a typical solution architecture. 
- **Sources:** We might have a diverse number of data sources like CSV files, managed and unmanaged relational data stores like Cassandra or DynamoDB. There could also be EC2 machines. 
- **ETL:**  Then, we would have our ETL servers, a class of products that communicate with all the data sources. 
- **Data Warehouse:** ETL server scripts and products issue commands to extract data from the sources and into S3 staging, as well as pulling the data into Redshift.
- **OLAP Cubes:** Once the data is loaded into Redshift, we are able to connect business intelligence apps and visualizations to it. Data cubes containing pre-aggregated data can also be materialized into Amazon S3.
- **BI Apps:** BI apps can work directly from Redshift or faster from these pre-aggregated OLAP cubes.

![Redshift Architecture and Dataflow](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/c484f32f02ab4808d5908823c4777890278c382d/Images/redshift-architecture-and-dataflow.jpg)

### Transferring Data from an S3 Staging Area to Redshift

Use the ``COPY`` Command:

- Inserting data row by using ``INSERT`` will be very slow
- Performs a bulk upload of data

If the file is large:

-   It is better to break it up into multiple files
-   Ingest in Parallel. How?
	- The files have a common prefix
	- Using a Manifest file
- Use compression from the beginning in ``gzip`` format

Other considerations:

-   Better to ingest from the same AWS region
-   Better to compress all the CSV files

Let's take a look at an example of using a common prefix with a copy command. Will copy to a target table in Redshift from a particular S3 bucket. Here, we have an S3 bucket and a key that consists of a path, and at the end you have a part. This part is not a file. 

If you look at the structure of this ticket's split key, it consists of 10 files, and these 10 files have a common prefix.

Redshift will parallelize the processing of the data based on the prefix. It will spin up a number of workers, and these compute nodes can adjust the file into Redshift in parallel.

Redshift is initiating a connection to S3 to fetch the data, so you'll need credentials to be able to access Amazon S3 from Redshift.

You can declare the use of gzip as well as accustomed delimiter, in this case, a semicolon and the AWS region in which the data is stored.
![Ingesting with Prefix](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/c484f32f02ab4808d5908823c4777890278c382d/Images/ingesting-with-prefix.jpg)

If you do not want to depend on a prefix and you want to be more explicit, you can use a manifest method to copy into a table with the copy command.
![Ingesting with Manifest](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/c484f32f02ab4808d5908823c4777890278c382d/Images/ingesting-with-manifest.jpg)



## Optimizing Table Design with Distribution Styles

We want to optimize the design of our tables where we ingest data in order to speed up queries.

Big tables are partitioned into smaller partitions so that we can access them in parallel and parallelize them in slices. If you have information about the frequent access pattern of a table, you can choose a more optimized strategy.

The two possible strategies are:
1. **Distribution style:** 
	- EVEN distribution
	- ALL distribution
	- AUTO distribution
	- KEY distribution
2. **Sorting keys**

### Distribution Styles
**EVEN Distribution**
Let's start with <u>Even Distribution</u>. Let's say we have a table containing 1,000 rows. It has a primary key and a reference to a dimension which is a store, dim store in this example. We start copying this into a table, and to Redshift, we are copying the file in parallel, and Redshift will load balance the amounts of data being copied.

Ideally, if there are 1,000 rows, we would want 250 rows on each slice of compute using an even or round-robin distribution style. Each server is given the same amount of rows and that evens out the load.

![EVEN Distribution](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/f7965206808be904e5e7233d3fbf85ee0b482282/Images/even-distribution.jpg)

**ALL Distribution**
Let's look at an example where we have a smaller table with only 40 rows. That is a dimension table for the stores. When we copy the table, what is going to happen if we join the facts and the dimension to get the store information itself, which is either New York or California? It would be optimal if all the foreign keys resided on the same machine. Imagine tables with thousands or millions of rows. The distribution of all these keys is called **shuffling**. When we join a table using an even strategy, we do lots of shuffling.

![ALL Distribution](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/f7965206808be904e5e7233d3fbf85ee0b482282/Images/all-distribution.jpg)

There are distribution styles to optimize the shuffling. In the distribution style, small tables are replicated on all slices to speed up joins. In general, there are not a lot of rows and dimensional tables compared to fact tables. The all-distribution style is also known as **broadcasting** because it broadcasts the replicated table across the cluster.

Using the previous example, the Fact Sales tables are still distributed using the even strategy, but the store dimension is replicated using the all strategy. Using the all-distribution style for the store dimension minimizes traversing and shuffling.

![Distributing Facts with EVEN and Dimensions with ALL](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/f7965206808be904e5e7233d3fbf85ee0b482282/Images/distributing-facts-dimensions.jpg)


**AUTO Distribution**
A third distribution style is called <u>AUTO Distribution</u>. Auto distribution leaves the decision to Redshift. Small tables are distributed with an all-strategy. Redshift does the calculations to determine which small tables are optimal to broadcast. Large tables are distributed using an even strategy. 

**KEY Distribution**
The last distribution style we'll cover is the <u>KEY Distribution</u> strategy. In this distribution, rows having similar values are placed in the same slice. In this example, a fact table is distributed on the dim store key. Keys are grouped on partitions, which can sometimes lead to a skewed distribution if some values of the key are more frequent than others. 

![KEY Distribution](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/f7965206808be904e5e7233d3fbf85ee0b482282/Images/key-distribution.jpg)

Here's what the SQL syntax looks for for declaring a distribution key on a fact table and dimension table. After the not null, we declare a distribution key used to join the tables. 

![KEY Distribution SQL](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/f7965206808be904e5e7233d3fbf85ee0b482282/Images/key-distribution-sql.jpg)


### Sorting Keys
Another distribution optimization is using sorting keys. You can define a column as a sort key. If you choose one column to be a sort key, when data's copied, rows are sorted before distribution to slices. This minimizes query time since each node already has contiguous ranges of rows based on the sorting keys. It is useful for columns that are frequently used in order by queries which are typically found in fact tables.

![Sorting Keys](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/f7965206808be904e5e7233d3fbf85ee0b482282/Images/sorting-distribution.jpg)

A column can be both a distribution key and a sort key. If you order by a field a lot, you might want to mark it as a sort key. Here's what the syntax looks like in SQL. In this example, the order date is marked as a sort key. The primary key of the dimensions table could be a sort key and a distribution key. 

![Sorting Keys SQL](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/f7965206808be904e5e7233d3fbf85ee0b482282/Images/sorting-distribution-sql.jpg)
