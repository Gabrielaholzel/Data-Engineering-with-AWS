# Implementing a Data Warehouse on AWS

## Amazon Redshift

Redshift is a **column-oriented RDBMS** that is best suited of online analytical processing (OLAP) workloads. A key difference is the way queries are executed. Most relational databases will execute multiple queries in parallel if they have access to many cores or servers. If you have an RDBMS database cluster, many queries can run at the same time, but each query runs on only one CPU. If there're a lot of concurrent users running queries, they can be scheduled on CPUs. This turns out to be appropriate for OLTP applications because there are a lot of concurrent users, each running small queries, like an update or retrieving a few rows. 

When you're building a data warehouse solution though, and dealing with large amounts of data, you'll need a database capable of **massive parallel processing (MPP)**. MPP databases like Amazon Redshift parallelise the execution of a single query on multiple CPUs and multiple machines. 

Tables in MPP databases are partitioned into smaller partitions and distributed across CPUs and each CPU also has its own associated storage. One query can process a whole table in parallel and each CPU is processing only one partition of the data. 

Redshift is a cluster of machines composed of one leader node and one or more compute nodes. You can run a cluster with a single node, though. The leader node interacts with the outside world. Client applications talk to the leader node using protocols like JDBC or ODBC. To them, it's like any other normal database. 

However, under the hood, the leader node commands a number of compute nodes. The leader node coordinates the work of these compute nodes. It handles external communication and optimises query execution. 

Each compute node has its own CPU, memory and disk, and you can configure how powerful the cluster will be, as well as configuring whether you want to scale up or scale out. **Scaling up** means adding more nodes and **scaling out** means fewer but larger nodes. Each compute node is logically divided into a number of slices. For simplicity, you can think of a slice as a CPU with many disks dedicated to its work. A cluster with n slices can process n partitions of a table simultaneously. <u>The sum of all slices across all compute nodes is the unit of parallelisation, i.e. the total number of slices in a cluster is equal to the sum of all slices on the cluster</u>. 

If you have a Redshift cluster with a dc1 large EC2 instance which has two CPUs, it'll have two slices. It has 15 gigabytes of RAM and a 60 gigabyte solid-state drive. You can have from 1 to 32 in a cluster, giving you a total capacity of around five terabytes. 

You can also choose storage optimised nodes. These nodes are not as fast or powerful in terms of CPU, but they are larger in capacity. One of these has 36 CPUs. You can configure up to 128, giving you a capacity around two petabytes. However, these instances are rather expensive. For example, a dc2 large instance costs $0.25 per hour. If you use four of these in a cluster, you'll pay $1 per hour, so it's very important to stop or delete these resources if you're not using them. 



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
