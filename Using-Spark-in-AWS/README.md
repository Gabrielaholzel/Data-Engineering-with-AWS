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




## Glue Studio

We started off by introducing Spark, then RDDs, and then Spark SQL. Spark SQL relies on RDDs, which rely on Spark itself. Similarly, Glue is an AWS Service that relies on Spark. You can use Glue Studio to write purely Spark scripts. We will also go over unique Glue features you can add to your script.

Using AWS Glue to run Spark Jobs requires the following resources and configuration:

![Glue Job Using S3 VPC Gateway](https://video.udacity-data.com/topher/2022/September/631d9060_l4-using-spark-in-aws-2/l4-using-spark-in-aws-2.jpeg)

Glue Job Using S3 VPC Gateway

#### Routing Table

A routing table is an entity that stores the network paths to various locations. For example, it will store the path to S3 from within your VPC. You'll need a routing table to configure with your VPC Gateway. You will most likely only have a single routing table if you are using the default workspace.

#### VPC Gateway

Your cloud project runs resources within a Virtual Private Cloud (VPC). This means your Glue Job runs in a Secure Zone without access to anything outside your Virtual Network. For security reasons, this is very sensible. You don't want your glue job accessing resources on the internet, for example, unless you specifically require it.

A VPC Gateway is a network entity that gives access to outside networks and resources. Since S3 doesn't reside in your VPC, you need a VPC Gateway to establish a secure connection between your VPC and S3. This allows your Glue Job, or any other resources within the VPC, to utilize S3 for data storage and retrieval.

#### S3 Gateway Endpoint

By default, Glue Jobs can't reach any networks outside of your Virtual Private Cloud (VPC). Since the S3 Service runs in different network, we need to create what's called an S3 Gateway Endpoint. This allows S3 traffic from your Glue Jobs into your S3 buckets. Once you have created the endpoint, your Glue Jobs will have a network path to reach S3.

#### S3 Buckets

Buckets are storage locations within AWS, that have a hierarchical directory-like structure. Once you create an S3 bucket, you can create as many sub-directories, and files as you want. The bucket is the "parent" of all of these directories and files.



## Configuring the S3 VPC Gateway Endpoint

### Configuring AWS Glue: S3 VPC Gateway Endpoint

#### Step 1: Creating an S3 Bucket

Buckets are storage locations within AWS, that have a hierarchical directory-like structure. Once you create an S3 bucket, you can create as many sub-directories, and files as you want. The bucket is the "parent" of all of these directories and files.

To create an S3 bucket use the  `aws s3 mb`  command:  `aws s3 mb s3://_______`  replacing the blank with the name of your bucket. You can also create S3 buckets using the AWS web console.

#### Step 2: S3 Gateway Endpoint

By default, Glue Jobs can't reach any networks outside of your Virtual Private Cloud (VPC). Since the S3 Service runs in different network, we need to create what's called an S3 Gateway Endpoint. This allows S3 traffic from your Glue Jobs into your S3 buckets. Once we have created the endpoint, your Glue Jobs will have a network path to reach S3.

First use the AWS CLI to identify the VPC that needs access to S3:

`aws ec2 describe-vpcs`

The output should look something like this (look for the VpcId in the output):

  
```JSON
`{
    "Vpcs": [
        {
            "CidrBlock": "172.31.0.0/16",
            "DhcpOptionsId": "dopt-756f580c",
            "State": "available",
            "VpcId": "vpc-7385c60b",
            "OwnerId": "863507759259",
            "InstanceTenancy": "default",
            "CidrBlockAssociationSet": [
                {
                    "AssociationId": "vpc-cidr-assoc-664c0c0c",
                    "CidrBlock": "172.31.0.0/16",
                    "CidrBlockState": {
                        "State": "associated"
                    }
                }
            ],
            "IsDefault": true
        }
    ]
}
```


### Routing Table

Next, identify the routing table you want to configure with your VPC Gateway. You will most likely only have a single routing table if you are using the default workspace. Look for the RouteTableId:

`aws ec2 describe-route-tables`

```JSON
{
	"RouteTables":  [
		{
		.  .  .  
			"PropagatingVgws":  [],
			"RouteTableId":  "rtb-bc5aabc1",
			"Routes":  [
				{
					"DestinationCidrBlock":  "172.31.0.0/16",
					"GatewayId":  "local",
					"Origin":  "CreateRouteTable",
					"State":  "active"
				}
			],
			"Tags":  [],
			"VpcId":  "vpc-7385c60b",
			"OwnerId":  "863507759259"
		}
	]
}
```

#### Create an S3 Gateway Endpoint

Finally create the S3 Gateway, replacing the blanks with the  **VPC**  and  **Routing Table Ids**:

`aws ec2 create-vpc-endpoint --vpc-id _______ --service-name com.amazonaws.us-east-1.s3 --route-table-ids _______`


### Creating the Glue Service IAM Role

AWS uses Identity and Access Management (IAM) service to manage users, and roles (which can be reused by users and services). A Service Role in IAM is a Role that is used by an AWS Service to interact with cloud resources.

![Glue Job Using S3 VPC Gateway](https://video.udacity-data.com/topher/2022/September/631d938e_l4-using-spark-in-aws/l4-using-spark-in-aws.jpeg)

Glue Job Using S3 VPC Gateway

For AWS Glue to act on your behalf to access S3 and other resources, you need to grant access to the Glue Service by creating an IAM Service Role that can be assumed by Glue:

```python
aws iam create-role --role-name my-glue-service-role --assume-role-policy-document '{
	"Version":  "2012-10-17",
	"Statement":  [
		{
			"Effect":  "Allow",
			"Principal":  {
				"Service":  "glue.amazonaws.com"
			},
			"Action":  "sts:AssumeRole"
		}
	]
}'
```


#### Grant Glue Privileges on the S3 Bucket

Replace the two blanks below with the S3 bucket name you created earlier, and execute this command to allow your Glue job read/write/delete access to the bucket and everything in it. You will notice the S3 path starts with  `arn:aws:s3:::`  . An ARN is an AWS Resource Name. The format is generally:

`arn:[aws/aws-cn/aws-us-gov]:[service]:[region]:[account-id]:[resource-id]`

You may notice that after  `s3`  there are three colons  `:::`  without anything between them. That is because S3 buckets can be cross-region, and cross AWS account. For example you may wish to share data with a client, or vice versa. Setting up an S3 bucket with cross AWS account access may be necessary.

**Replace the blanks in the statement below with your S3 bucket name (ex: seans-lakehouse)**  
`aws iam put-role-policy --role-name my-glue-service-role --policy-name S3Access --policy-document '{ "Version": "2012-10-17", "Statement": [ { "Sid": "ListObjectsInBucket", "Effect": "Allow", "Action": [ "s3:ListBucket" ], "Resource": [ "arn:aws:s3:::_______" ] }, { "Sid": "AllObjectActions", "Effect": "Allow", "Action": "s3:*Object", "Resource": [ "arn:aws:s3:::_______/*" ] } ] }'`

## Spark Jobs

Jupyter notebooks are great for prototyping as well as exploring and visualizing your data. However, Jupyter notebooks aren't the best tool for automating your workflow, that's where Python scripts come into play.

Imagine you work for a social media company that receives a constant stream of text, image, and video data from your users. To keep up with your users, you want your Spark jobs to run automatically at specific intervals, perhaps once every hour. These Spark jobs give your entire team the latest information on their users and will probably become so useful to your team that they will start to request more and more Spark jobs. You won't want to manually run a growing collection of notebooks, you'll want automated scripts that you can set and forget. We will be using Glue Studio to write Spark jobs that can be automated, and set to run at certain intervals.

![Running Spark scripts at a time interval](https://video.udacity-data.com/topher/2021/September/6140d3da_screen-shot-2021-09-14-at-11.54.36-am/screen-shot-2021-09-14-at-11.54.36-am.png)

# Create a Spark Job using Glue Studio

![Glue Studio Flow Diagram](https://video.udacity-data.com/topher/2022/September/631f9e58_l4-using-spark-in-aws-1/l4-using-spark-in-aws-1.jpeg)

## Using Glue Studio to Create Spark Jobs

Glue Studio is a Graphical User Interface (GUI) for interacting with Glue to create Spark jobs with added capabilities. Glue APIs give access to things like Glue Tables, and Glue Context. These APIs are designed to enhance your Spark experience by simplifying development.

You can create Glue Jobs by writing, and uploading python code, but Glue Studio also provides a drag and drop experience. When you create a flow diagram using Glue Studio, it generates the Python or Scala Code for you automatically. The code is stored with additional configuration for running in Spark, including third-party libraries, job parameters, and the AWS IAM Role Glue uses.

![Sample Glue Studio Job](https://video.udacity-data.com/topher/2023/October/653c5e6c_1-customer_landing_to_trusted/1-customer_landing_to_trusted.jpeg)

Sample Glue Studio Job

### Glue Studio Visual Editor

The Glue Studio Visual Editor allows you to select three types of nodes when creating a pipeline:

-   Source- the data that will be consumed in the pipeline
-   Transform - any transformation that will be applied
-   Target - the destination for the data

### Sources

A common source is an S3 location or a Glue Table. But a source can be any AWS Database including:

-   Amazon S3
-   AWS Glue Data Catalog
-   Amazon DynamoDB
-   Amazon Kinesis
-   Apache Kafka
-   Amazon Redshift
-   MySQL
-   PostgreSQL
-   Microsoft SQL Server
-   Oracle SQL
-   Snowflake
-   Google BigQuery

### Transform

Common transformations include Joins, Field Mapping, and Filter. Custom SQL statements are also supported. Here is a list of some of the transformations available:

-   Apply Mapping
-   Select Fields
-   Drop Fields
-   Drop Null Fields
-   Drop Duplicates
-   Rename Field
-   Spigot
-   Join
-   Split Fields
-   Select from Collection
-   Filter
-   Union
-   Aggregate
-   Fill Missing Values
-   Custom Transform
-   Custom SQL
-   Detect PII

### Targets

All of the source types are also supported as targets. We will discuss more in this course about how to organize S3 storage and catalog it as Glue Tables in a way that keeps data logically separated.

### Create a Spark Job with Glue Studio

To use Glue Studio, search for it in the AWS Console. Then click the  **AWS Glue Studio**  menu option.

![Glue Studio in the AWS Console](https://video.udacity-data.com/topher/2022/June/62bc4026_screen-shot-2022-06-29-at-6.05.29-am/screen-shot-2022-06-29-at-6.05.29-am.jpeg)

Glue Studio in the AWS Console

Select either  **ETL Jobs**  or  **Visual ETL**  from the Glue Studio Menu

![AWS Glue Studio Menu](https://video.udacity-data.com/topher/2023/October/653c6643_2-menu/2-menu.jpeg)

AWS Glue Studio Menu

Select  **Jobs**  from the Glue Studio Menu

![AWS Glue Studio Menu](https://video.udacity-data.com/topher/2022/June/62bc40a4_screen-shot-2022-06-29-at-6.07.03-am/screen-shot-2022-06-29-at-6.07.03-am.jpeg)

AWS Glue Studio Menu

To get started, go with the default selection -  **Visual with a source and a target,**  and click  **Create**

![AWS Glue Studio Create Job](https://video.udacity-data.com/topher/2022/June/62bc41a7_screen-shot-2022-06-29-at-6.12.11-am/screen-shot-2022-06-29-at-6.12.11-am.jpeg)

AWS Glue Studio Create Job

Before we forget, under  **Job Details**  create a  **name**  for the Job, and choose the  **IAM Role**  the job will use during execution. This should be the Glue Service Role you created earlier.

![Glue Job Details](https://video.udacity-data.com/topher/2022/June/62bc442c_screen-shot-2022-06-29-at-6.22.59-am/screen-shot-2022-06-29-at-6.22.59-am.jpeg)

Glue Job Details

### Extract and Load Customer Data

Let's assume a website creates a daily JSON file of all new customers created during the previous 24 hours. That JSON file will go into the S3  **landing zone**  designated for new data. A landing zone is a place where new data arrives prior to processing.

We can copy a sample customer file into S3 using the the AWS Command Line Interface (CLI). In the command below the blank should be replaced with the name of the S3 bucket you created:

`aws s3 cp ./project/starter/customer/landing/customer-1691348231425.json s3://_______/customer/landing/`

### Privacy Filter

One of the most important transformations is excluding Personally Identifiable Information (PII). Glue has an out-of-the-box filter, but we are going to make our own. For the  **source**  in your Glue Studio Job, choose the S3 bucket you created earlier, with the folder containing the  **raw**  or  **landing**  customer data. The folder should have a forward-slash / on the end.

Click on the  `+`  button, then pick  **Amazon S3**  from the  **Source**  tab

  
  

![Choose Source as Amazon S3](https://video.udacity-data.com/topher/2023/October/653c68a2_3-privacy_filter-1/3-privacy_filter-1.jpeg)

Choose Source as Amazon S3

_Under Node properties, name the Data source appropriately, for example: Customer Landing or Customer Raw._

![Customer Data Source (Landing Zone)](https://video.udacity-data.com/topher/2023/October/653c68f9_4-privacy_filter-2/4-privacy_filter-2.jpeg)

Customer Data Source (Landing Zone)

For the  **transformation**, select the  **filter**  option

![Filter Option](https://video.udacity-data.com/topher/2023/October/653c694e_filter_option/filter_option.jpeg)

Filter Option

Filter on the  _shareWithResearchAsOfDate_  timestamp field, and configure it to filter out customers that have an empty zero_shareWithResearchAsOfDate_.

_Name the Transform appropriately, for example: Share With Research_

![Privacy Filter](https://video.udacity-data.com/topher/2023/October/653c6992_5-privacy_filter-3/5-privacy_filter-3.jpeg)

Privacy Filter

For your destination choose an S3 location for customers who have chosen to share with research, or a  **trusted zone**. The S3 bucket should be the bucket you created earlier. Any time you specify a folder that doesn't exist, S3 will automatically create it the first time data is placed there. Be sure to add the forward-slash on the end of the folder path.

![Customer Data Target (Trusted Zone)](https://video.udacity-data.com/topher/2023/October/653c69fa_6-privacy_filter-4/6-privacy_filter-4.jpeg)

Customer Data Target (Trusted Zone)

### Save and Run the Job

You will notice the red triangle at the top of the screen saying "**Job has not been saved**."

Click the Save button, then click Run:

![Save and Run the Job](https://video.udacity-data.com/topher/2022/June/62bc4e48_screen-shot-2022-06-29-at-7.06.08-am/screen-shot-2022-06-29-at-7.06.08-am.jpeg)

Save and Run the Job

On the green ribbon, click the  **Run Details**  link

![Click Run Details](https://video.udacity-data.com/topher/2022/June/62bc4ed3_screen-shot-2022-06-29-at-7.08.17-am/screen-shot-2022-06-29-at-7.08.17-am.jpeg)

Click Run Details

You will then see the run details. By default the job will run three times before quitting. To view the logs, click the  **Error Logs**  link. This includes all of the non-error logs as well.

![Run Details](https://video.udacity-data.com/topher/2022/June/62bc4f5f_screen-shot-2022-06-29-at-7.09.29-am/screen-shot-2022-06-29-at-7.09.29-am.jpeg)

Run Details

To see the logs in real-time, click the  **log stream id**

![Log Streams](https://video.udacity-data.com/topher/2022/June/62bc5077_screen-shot-2022-06-29-at-7.14.51-am/screen-shot-2022-06-29-at-7.14.51-am.jpeg)

Log Streams

If the log viewer stops, click the  **resume**  button. It often pauses if the output takes more than a couple of seconds to progress to the next step. Notice that most of the output in this example is INFO. If you see a row marked as ERROR, you can expand that row to determine the error:

![Job Log output](https://video.udacity-data.com/topher/2022/June/62bc50f3_screen-shot-2022-06-29-at-7.16.29-am/screen-shot-2022-06-29-at-7.16.29-am.jpeg)

Job Log output

### View the Generated Script

To view the generated script, go back to Glue Studio, and click the  **Script**  tab:

![Glue Script](https://video.udacity-data.com/topher/2022/June/62bc52ef_screen-shot-2022-06-29-at-7.25.54-am/screen-shot-2022-06-29-at-7.25.54-am.jpeg)

Glue Script

In this project, you will create tables from your S3 files.

We will later revisit this Glue Job and change the option to Create a table in the Data Catalog and on subsequent runs, update the schema and add new partitions. With this, the Glue Job will create a table and update the metadata on subsequent runs.

  

_Important_

Glue Jobs does not delete any data stored in the S3 bucket. You must manually delete the files when you need to re-run your Glue Jobs.

### Save and Run the Job

  

You will notice the red triangle at the top of the screen saying "Job has not been saved."

  

Click the Save button, then click Run:

![Run the Job](https://video.udacity-data.com/topher/2022/July/62da967b_screen-shot-2022-07-22-at-6.21.56-am/screen-shot-2022-07-22-at-6.21.56-am.jpeg)

Run the Job



# Storing and Retrieving Data on the Cloud

## Using S3 to Read and Write Data

One of the most common places to store big data sets is Amazon's Simple Storage Service or S3 for short. Amazon S3 is a safe, easy, and cheap place to store big data. Amazon does all the work of maintaining the hardware, keeping backups, and making sure the data is almost always available. You can think about it like Dropbox or iCloud for your big data. You don't need to worry about the details of how S3 works, the Amazon engineers take care of that. You just need to know how to use S3 with Spark. So, next, we will show you how to store data in S3 and then retrieve the data for your Spark program.

### Using Glue Dynamic Frames to Read S3

Glue adds the concept of a Dynamic Frame to Spark, which is very similar to a Data Frame. Data Frames can be converted to Dynamic Frames and vice versa.

### Using S3 Buckets to Store Data

S3 stores an object, and when you identify an object, you need to specify a bucket, and key to identify the object. In Glue jobs, you can still use Spark Data Frames.

For example,

 ```python
 df = spark.read.load(“s3://my_bucket/path/to/file/file.csv”)
 ``` 

From this code,  `s3://my_bucket`  is the bucket, and  `path/to/file/file.csv`  is the key for the object. Thankfully, if we’re using Spark and all the objects underneath the bucket have the same schema, you can do something like the following.

 ```python
df  = spark.read.load(“s3://my_bucket/”)
```

This will generate a dataframe of all the objects underneath the  `my_bucket`  with the same schema.

Imagine you have a structure in S3 like this:

 ```python
 my_bucket
	 |---test.csv
	 path/to/
		 |--test2.csv
		 file/
			 |--test3.csv
			 |--file.csv
 ``` 

**If all the csv files underneath  `my_bucket`, which are  `test.csv`,  `test2.csv`,  `test3.csv`, and  `file.csv`  have the same schema, the DataFrame will be generated without error, but if there are conflicts in schema between files, then the DataFrame will not be generated.**



## Differences between HDFS and AWS S3

### Differences between HDFS and AWS S3

Since Spark does not have its own distributed storage system, it leverages HDFS or AWS S3, or any other distributed storage. Primarily in this course, we will be using AWS S3, but let’s review the advantages of using HDFS over AWS S3.

-   **AWS S3**  is an  **object storage system**  that stores the data using key value pairs, and  **HDFS**  is an  **actual distributed file system**  that guarantees fault tolerance. HDFS achieves fault tolerance by duplicating the same files at 3 different nodes across the cluster by default (it can be configured to reduce or increase this duplication).
-   HDFS has traditionally been installed in on-premise systems which had engineers on-site to maintain and troubleshoot the Hadoop Ecosystem,  **costing more than storing data in the cloud**. Due to the flexibility of location and reduced cost of maintenance, cloud solutions have been more popular. With the extensive services AWS provides, S3 has been a more popular choice than HDFS.
-   Since  **AWS S3 is a binary object store**, it can  **store all kinds of formats**, even images and videos. HDFS strictly requires a file format - the popular choices are  **avro**  and  **parquet**, which have relatively high compression rates making it useful for storing large datasets.
