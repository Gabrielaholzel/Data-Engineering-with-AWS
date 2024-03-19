# Using Spark in AWS

## Data Lakes in AWS

### Data Lakes are Natural

It doesn't have to be called a data lake to be one! Many lakes and other natural features existed for thousands of years without being discovered. But they still existed. Perhaps you are about to discover a data lake you didn't recognize.

A lake is a large body of water. It is usually a naturally occurring feature. If your organization has large amounts of data somewhere, in an  **unstructured**  (Text, Multimedia, etc.) or  **semi-structured**  format (CSV, JSON, Parquet, and other formats), congratulations! You have a  **data lake**!

![SFTP or S3 Watering Hole](https://video.udacity-data.com/topher/2022/July/62d00bf5_screen-shot-2022-07-14-at-6.28.27-am/screen-shot-2022-07-14-at-6.28.27-am.jpeg)

SFTP or S3 Watering Hole

#### The Watering Hole

A classic example of a naturally occurring data lake is an old-fashioned  **SFTP**  **(Secure File Transfer Protocol)**  server. SFTP servers are network-connected servers, that make file storage available on a network (similar to S3 buckets).

SFTP servers and S3 buckets enable systems and people to exchange data in specific directories. These directories usually have a  **landing**  directory for new, unprocessed files. Once the files are processed, they are moved to a  **processed**  directory.

The processed files are kept for record-keeping purposes. If a file needs to be re-processed due to an error, the file can be copied or moved from the  **processed**  directory to the  **landing**  folder.

In the example shown above, the Slow But Cheap Taxi company can drop their invoice files off in the  **landing**  directory, which will be paid and processed automatically. Then the invoices files are moved to the  **processed**  directory.

If the taxi company wants to know if their invoice has been paid, they can look in the processed directory.

#### Why do data lakes exist?

As data evolves, so do the systems supporting them. We live in an era of unprecedented data production, storage, and accumulation. The rate at which our society produces data is phenomenal. Subscribe to a Twitter or Reddit feed, or surf YouTube. There are millions of channels and billions of posts!

The need to store all of that data is increasing by the second. Over ten years ago,  **HDFS**  was born to help deal with the challenge of storing a file that couldn't actually fit  **anywhere**. The idea was simple: if a file can't fit on a single server, make it work like it is on a single server, but split the file up across a cluster of servers.

#### Data Lakes in the AWS Cloud

Data Lakes are not a specific technology. They can be implemented using many types of file storage systems. In AWS, the most common way to store files is in S3, so we can implement data lakes using S3 storage.

#### S3 Data Lakes and Spark on AWS

Like the Hadoop Distributed File System, AWS created  **S3**, the  [**Simple Storage Service**(opens in a new tab)](https://aws.amazon.com/s3/). S3 buckets are an abstraction of storage similar to HDFS. They make it possible to store an almost unlimited amount of data and files.

S3 doesn't require the maintenance required by most file storage systems. It is relatively easy to use. The very top level of S3 is called an  **S3 Bucket**. Within a bucket, you can keep many directories and files.

Because S3 has almost unlimited storage capacity and is very inexpensive, it is the ideal location to store data for your data lake. Compared with the cost of other more sophisticated data locations such as RDS, and EC2, S3 is much cheaper. There is no compute cost associated with S3 by default. So if you just need a place to store large amounts of files, this is a great place for them.

![Lakes are naturally occuring repositories of data for sharing](https://video.udacity-data.com/topher/2022/September/631d898b_noun-lake-5067600-02b3e4/noun-lake-5067600-02b3e4.jpeg)

Lakes are naturally occuring repositories of data for sharing



## Using Spark on AWS

When you want to rent a cluster of machines on AWS to run Spark, you have several choices:

-   EMR - EMR is an AWS managed Spark service a scalable set of EC2 machines already configured to run Spark. You don't manage the systems, only configure the necessary cluster resources.
-   EC2 - Use AWS Elastic Compute (EC2) machines and install and configure Spark and HDFS yourself.
-   Glue - Glue is a serverless Spark environment with added libraries like the Glue Context and Glue Dynamic Frames. It also interfaces with other AWS data services like Data Catalog and AWS Athena.

In this course, we'll focus on using the AWS Glue tool to run Spark scripts, but you can find more information about the EMR and EC2 options below.

### Differences between Spark on AWS EC2 vs EMR

![Differences between Spark on AWS EC2 vs EMR](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/e0155f1280853a162d576b1abd8ce5e73179cb61/Images/differences-between-spark-on-AWS-EC2-vs-EMR.jpg)

### Circling Back on HDFS

Since Spark does not have its own distributed storage system, it leverages using HDFS or AWS S3, or any other distributed storage. Primarily in this course, we will be using AWS S3, but let’s review the advantages of using HDFS over AWS S3.

### What is HDFS?

HDFS (Hadoop Distributed File System) is the file system in the Hadoop ecosystem. Hadoop and Spark are two frameworks providing tools for carrying out big-data related tasks. While Spark is faster than Hadoop, Spark has one drawback. It lacks a distributed storage system. In other words, Spark lacks a system to organize, store and process data files.

### MapReduce System

HDFS uses MapReduce system as a resource manager to allow the distribution of the files across the hard drives within the cluster. Think of it as the MapReduce System storing the data back on the hard drives after completing all the tasks.

Spark, on the other hand, runs the operations and holds the data in the RAM memory rather than the hard drives used by HDFS. Since Spark lacks a file distribution system to organize, store and process data files, Spark tools are often installed on Hadoop because Spark can then use the Hadoop Distributed File System (HDFS).

### Why Would You Use an EMR Cluster?

Since a Spark cluster includes multiple machines, in order to use Spark code on each machine, we would need to download and install Spark and its dependencies. This is a manual process. AWS  **EMR**  is a service that negates the need for you, the user, to go through the manual process of installing Spark and its dependencies for each machine.
