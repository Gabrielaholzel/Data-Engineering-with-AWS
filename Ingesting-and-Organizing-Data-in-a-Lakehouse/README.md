# Lakehouse Architecture

## The Lakehouse

The  **Lakehouse**  is another evolution of data storage. The purpose of a Lakehouse is to separate data processing into stages. Like an oil refinery, data is staged and processed step by step until it becomes available for querying.

Lakehouse is not a specific technology. It can be implemented using any file storage and processing layer. In AWS, the most common way to store files is in S3, so we can implement the Lakehouse using S3 storage.

![Lakehouse](https://video.udacity-data.com/topher/2022/September/6320fd4f_l5-ingesting-and-organizing-data-in-a-lakehouse/l5-ingesting-and-organizing-data-in-a-lakehouse.jpeg)

### Lakehouse Zones

Think about our invoice example earlier. An accounting system is the destination for the files in the landing directory. That accounting system is responsible for extracting the invoices from the invoice files, transforming them into the correct format, and loading them into the accounting database where they can be paid. These steps are known as  **ETL (Extract, Transform, and Load).**  With ETL, usually data is going from a semi-structured (files in directories) format to a structured format (tables).

With  **ELT**, however, and with a Lakehouse, the data stays in semi-structured format, and the last zone contains enriched data where it can be picked up for processing later. Deferring transformation is a hallmark of Data Lakes and Lakehouses. In this way, keeping the data at multiple stages in file storage gives more options for later analytics, because it preserves all of the format. What if the accounting system had a defect that didn't load data properly for certain vendors. The original data is still available to be analyzed, transformed, and re-processed as needed.

  

**Raw/Landing Zone**

"For pipelines that store data in the S3 data lake, data is ingested from the source into the landing zone as-is. The processing layer then validates the landing zone data and stores it in the raw zone bucket or prefix for permanent storage. "

----------

**Trusted Zone**

"The processing layer applies the schema, partitioning, and other transformations to the raw zone data to bring it to a conformed state and stores it in trusted zone."

----------

**Curated Zone**

**"**As a last step, the processing layer curates a trusted zone dataset by modeling it and joining it with other datasets, and stores it in curated layer."

"Typically, datasets from the curated layer are partly or fully ingested into Amazon Redshift data warehouse storage to serve use cases that need very low latency access or need to run complex SQL queries."

Source:  [(opens in a new tab)](https://aws.amazon.com/blogs/big-data/build-a-lake-house-architecture-on-aws/)[https://aws.amazon.com/blogs/big-data/build-a-lake-house-architecture-on-aws/(opens in a new tab)](https://aws.amazon.com/blogs/big-data/build-a-lake-house-architecture-on-aws/)

### Structure and Format

Because querying and reading data from S3 is billed by the gigabyte, optimizing those queries is a very good idea. Data can be compressed at a very high ratio, using  **gzip**  and other compression formats. Whenever possible, data in S3 should also be in a columnar format like  **parquet**  files. This means that when issuing queries to S3, the entire row of data doesn't need to be scanned to locate a single field. The query becomes more efficient and cheaper.


# Use Glue Catalog to Query a Landing Zone

## Tackle Boxes and Glue

Have you ever been fishing with an expert fisher? One thing you will notice is that they usually have something called a "Tackle Box." The Tackle Box has all of the bait and lures fishers can use to catch the varieties of fish they are looking for.

Looking inside the tackle box, you see a rainbow of colors, shapes, and sizes. This tackle box represents all the types of fish that can be caught. If they wanted to catch more types of fish, your fishing friend would add more lures or bait to their tackle box.

A  [Glue Data Catalog(opens in a new tab)](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html)  represents many sources and destinations for data. They can represent Kafka, Kinesis, Redshift, S3, and many more. If we want to connect to another data source, we must add it to the catalog. This makes querying data much easier because just like catching a fish, we know where to look for the type of data we are looking for.

### Glue Tables

A  [**Glue Table** (opens in a new tab)](https://docs.aws.amazon.com/glue/latest/dg/components-overview.html)  is a definition of a specific group of fields that represents a logical entity. The Glue Catalog is made up of multiple table definitions.  **These tables are not physically stored in Glue.**  _Glue tables are just a metadata catalog layer_. They store a reference to the data we can query or store.

There are  [multiple ways to create Glue Tables(opens in a new tab)](https://docs.aws.amazon.com/glue/latest/dg/tables-described.html), and we will focus on three ways to define a Glue Table in a Glue Catalog:

-   Use Glue Console to define each field
-   Configure a Glue Job to generate a table definition automatically
-   Use SQL to define a table with DDL (Data Definition Language) or create statements

### Using the Glue Console to Define a Table

Imagine you have the Customer data we looked at earlier in an S3 bucket directory, and you want to know how many records have been placed in the Customer Landing Zone. You could create a  **Glue Table**  definition to query the data using SQL.

Let's go over to the Glue Catalog in the Glue Console. Search for Glue Catalog in the AWS Console, and you will see the Glue Data Catalog. Click Data Catalog.

![Glue Catalog Menu](https://video.udacity-data.com/topher/2022/July/62c42815_screen-shot-2022-07-05-at-6.01.11-am/screen-shot-2022-07-05-at-6.01.11-am.jpeg)

Navigate to the side menu and select  _Databases_. Subsequently, initiate the database creation process by clicking the  _Add database_  button.

  

![Add database](https://video.udacity-data.com/topher/2023/December/65865879_screenshot-2023-12-23-091758/screenshot-2023-12-23-091758.jpeg)

Input your database name and click the  _Create database_  button.

  

![Database name](https://video.udacity-data.com/topher/2023/December/6586589b_screenshot-2023-12-23-091820/screenshot-2023-12-23-091820.jpeg)

Upon successful completion, you can view the newly created database in the list of databases.

![](https://video.udacity-data.com/topher/2023/December/658658c3_screenshot-2023-12-23-091917/screenshot-2023-12-23-091917.jpeg)

Now, let's proceed to generate a table. Navigate to the Tables option on the left side menu, and initiate the table creation process by selecting the  _Add table_  button.

  

![Add table manually](https://video.udacity-data.com/topher/2023/December/658658fe_screenshot-2023-12-23-092017/screenshot-2023-12-23-092017.jpeg)

Please provide the name of the table you're defining and specify the associated database.

  

![Enter table and database name](https://video.udacity-data.com/topher/2023/December/65865933_screenshot-2023-12-23-092106/screenshot-2023-12-23-092106.jpeg)

Here are the settings for the data source: please keep the source type as S3, as it is the default option, and indicate that the source is owned by my account. Lastly, input the path,  **s3://your-own-bucket-name/customer/landing/**. Be sure to replace “_your-own-bucket-name_” with the actual name of the bucket you previously created:

  

![Enter the full path to the folder for your customer landing zone](https://video.udacity-data.com/topher/2023/December/65865984_screenshot-2023-12-23-092231/screenshot-2023-12-23-092231.jpeg)


### Choose the data format

Choose JSON for the data format for your customer landing zone data, and click next

![Select the data format](https://video.udacity-data.com/topher/2023/December/658659a7_screenshot-2023-12-23-092304/screenshot-2023-12-23-092304.jpeg)

### Define the fields

Look at the sample JSON data below:

`{  "customerName":  "Santosh Clayton",  "email":  "Santosh.Clayton@test.com",  "phone":  "8015551212",  "birthDay":  "1900-01-01",  "serialNumber":  "50f7b4f3-7af5-4b07-a421-7b902c8d2b7c",  "registrationDate":  1655564376361,  "lastUpdateDate":  1655564376361,  "shareWithResearchAsOfDate":  1655564376361,  "shareWithPublicAsOfDate":  1655564376361,  "shareWithFriendsAsOfDate":  1655564376361  }`

Using the sample record above, define the fields in the glue table. You can input one entry by clicking the  _Add_  button.

  

![Define the fields using the sample record](https://video.udacity-data.com/topher/2023/December/65865a04_screenshot-2023-12-23-092437/screenshot-2023-12-23-092437.jpeg)



### Partition Indices

We can partition a table based on the index, or field, so that data is separated by category or other fields. For now we are going to skip this, click next, and then finish to confirm the table.

![Click finish to confirm](https://video.udacity-data.com/topher/2023/December/65865a25_screenshot-2023-12-23-092509/screenshot-2023-12-23-092509.jpeg)

### AWS Athena - a Glue Catalog Query Tool

Now that you have defined a table using the glue catalog, you might want to query the table. Previously we had to use Spark SQL and relied on Spark schemas to query data. Using the Glue Data Catalog, we can query data using an AWS tool called  [Athena(opens in a new tab)](https://aws.amazon.com/athena/). The Athena tool is a serverless query service where you can write SQL to run ad-hoc queries on S3 buckets.

Let's go over to Athena, and query the customer_landing_zone table:

![Search for Athena](https://video.udacity-data.com/topher/2022/July/62c437c7_screen-shot-2022-07-05-at-7.08.13-am/screen-shot-2022-07-05-at-7.08.13-am.jpeg)

Search for Athena

Athena uses S3 to store query results. Set up the location Athena will use from now going forward:

![Before you run your first query, you need to set up a query result location in Amazon S3.](https://video.udacity-data.com/topher/2022/July/62d95bc2_screen-shot-2022-07-21-at-7.59.11-am/screen-shot-2022-07-21-at-7.59.11-am.jpeg)

Notice the prompt

Click the View Settings button:

![View Settings](https://video.udacity-data.com/topher/2022/July/62d95c10_screen-shot-2022-07-21-at-8.00.30-am/screen-shot-2022-07-21-at-8.00.30-am.jpeg)



Enter the full S3 path you want Athena to save query results. Encryption makes it less likely that sensitive data will be compromised. For this exercise we will skip encryption:

![Query result location and encryption](https://video.udacity-data.com/topher/2022/July/62d95cd0_screen-shot-2022-07-21-at-8.03.49-am/screen-shot-2022-07-21-at-8.03.49-am.jpeg)

Enter an S3 location to store query results, click Save

Click the Editor tab:

![Query Editor](https://video.udacity-data.com/topher/2022/July/62d95e64_screen-shot-2022-07-21-at-8.10.31-am/screen-shot-2022-07-21-at-8.10.31-am.jpeg)



From this menu, click on the Create button and then choose S3 bucket data:

![Create table menu](https://video.udacity-data.com/topher/2023/November/65427582_6-create_table_menu/6-create_table_menu.jpeg)



Enter the table name you are creating, and choose "Create a database" if not already created, then type in the database name in which the table should reside

![Create the table and database](https://video.udacity-data.com/topher/2023/November/6542774c_7-create_table_and_db/7-create_table_and_db.jpeg)

Choose the directory that contains the physical landing zone data

![Customer landing zone location](https://video.udacity-data.com/topher/2023/November/654277f3_8-s3_path/8-s3_path.jpeg)



Choose JSON for the data format for your customer landing zone data, leave everything else as default

![JSON data Format options](https://video.udacity-data.com/topher/2023/November/654278d4_9-json/9-json.jpeg)



#### Define the fields

  

Look at the sample JSON data below:

`{ "customerName":"Frank Doshi",
"email":"Frank.Doshi@test.com",
"phone":"8015551212",
"birthDay":"1965-01-01",
"serialNumber":"159a908a-371e-40c1-ba92-dcdea483a6a2",
"registrationDate":1655293787680,
"lastUpdateDate":1655293787680,
"shareWithResearchAsOfDate":1655293787680,
"shareWithPublicAsOfDate":1655293787680,
"shareWithFriendsAsOfDate":1655293788443
}`

Using the sample record above, define the fields in the glue table, and click Create table

![Customer landing table definition](https://video.udacity-data.com/topher/2023/November/65427928_10-table_defs/10-table_defs.jpeg)



In the Editor tab, pick the database you have just created.

Enter a simple query like:  `select * from customer_landing`  and click run

![Simple query](https://video.udacity-data.com/topher/2022/July/62c43889_screen-shot-2022-07-05-at-7.10.50-am/screen-shot-2022-07-05-at-7.10.50-am.jpeg)



Now that you see results, you can use any desired SQL query parameters further refine your query and analyze the data in the landing zone:

![Query results](https://video.udacity-data.com/topher/2022/July/62c43956_screen-shot-2022-07-05-at-7.13.05-am/screen-shot-2022-07-05-at-7.13.05-am.jpeg)



# PII in the Landing Zone

## Ingesting Sensitive Data

Before we can process sensitive accelerometer data, we need to bring it into the  **landing zone**.

Using the AWS Cloudshell or CLI, copy the accelerometer data into an S3 landing zone with the  `s3 cp`  command (where the blank is the S3 bucket you created earlier):

`cd nd027-Data-Engineering-Data-Lakes-AWS-Exercises/project/starter aws s3 cp accelerometer/ s3://your-own-bucket-name/accelerometer/ --recursive`

Utilize AWS CloudShell or CLI to list the data in the landing zone, replacing "your-own-bucket-name" with the bucket name you created earlier in the course:

`aws s3 ls s3://your-own-bucket-name/accelerometer/landing/`

### Handling Sensitive Data

Data in the landing zone should be dealt with very carefully. It shouldn't be made available for analytics or business intelligence.

### Define a Glue Table for the Accelerometer Landing Zone

Now that you have some data in the landing zone you can define a glue table to make ad hoc querying easier. The landing zone should not be used for reporting or analytics, since the data is not qualified to be used for those purposes. However, you may want to get an idea of what the data looks like.

Go to Athena, select the database, and create a new table from S3 bucket data

![Create a table from S3 bucket data](https://video.udacity-data.com/topher/2022/July/62c82a93_screen-shot-2022-07-08-at-7.00.56-am/screen-shot-2022-07-08-at-7.00.56-am.jpeg)



Name the table something appropriate for the landing zone, choose the database, and enter a path  **ending with a slash**. As always, replace the “seans-stedi-lakehouse” of the S3 path with your own bucket name.

![S3 Table Settings](https://video.udacity-data.com/topher/2022/July/62c82caa_screen-shot-2022-07-08-at-7.09.48-am/screen-shot-2022-07-08-at-7.09.48-am.jpeg)



Choose the JSON data format, and add column names and types

![Define the Data](https://video.udacity-data.com/topher/2022/July/62c981b5_screen-shot-2022-07-09-at-7.24.58-am/screen-shot-2022-07-09-at-7.24.58-am.jpeg)

Preview the create table query and click  **create table**:

![Create Table](https://video.udacity-data.com/topher/2022/July/62c981d6_screen-shot-2022-07-09-at-7.25.26-am/screen-shot-2022-07-09-at-7.25.26-am.jpeg)



Copy the table query, and save it as accelerometer_landing.sql, then push it to your GitHub repository:

![Create Table Query](https://video.udacity-data.com/topher/2022/July/62c981ff_screen-shot-2022-07-09-at-7.26.07-am/screen-shot-2022-07-09-at-7.26.07-am.jpeg)

# Streaming Data Analysis

### Streaming Message Brokers

Spark is intended to process data that was previously generated. It doesn't process data in real time.  **Spark Streaming**  gives us the option of processing data in near real-time.

Often data is generated in real-time and then is stored for later processing. A common example is  **IoT**  or Internet of Things, which consists of small devices sending internet-connected messages. These devices send messages to convey meaning about the world. A smart thermostat is an IoT device. It continually communicates back with a server to send usage statistics to the end user.

Because servers are not always designed to handle large volumes of real-time data,  **message brokers**  were created. They are intended to "broker" connections between systems and make near real-time processing of data possible.

Some examples of message brokers are:

-   Kafka
-   Simple Queue Services (AWS SQS)
-   Amazon Kinesis

### Brokers aren't Forever

Message brokers don't last forever. Neither do the data they store. They are intended to facilitate a message being received and re-transmitted. This event typically should happen within seven days. Then the data will be deleted from the  **Raw Zone**.

To keep messages longer, we move them into a  **Landing Zone**. This is where the data can be loaded and transformed for later use in the  **Trusted**  and  **Curated Zone**.

![Streaming Data Processing](https://video.udacity-data.com/topher/2022/September/63215b09_l5-ingesting-and-organizing-data-in-a-lakehouse-1/l5-ingesting-and-organizing-data-in-a-lakehouse-1.jpeg)

### Using Glue to Process Streaming Data

Glue can load data directly from Kafka or Kinesis. AWS doesn't offer Glue support for SQS at this time. Using Spark Streaming, we can load data from Message Brokers into a Spark DataFrame or Glue DynamicFrame.

We can then join data from the Message Broker with other data sources as part of the streaming job to create  **Trusted**  or  **Curated data**. Kafka can be configured to load data into S3 using a Kafka Connector as a  **Landing Zone**, avoiding the need to connect Glue to Kafka directly.

# Curated Data

## Data Curation

Most museum have a curator, or a person who ensures the collection of artifacts meet the standards of the museum. For a Data Lake or Lakehouse, you are the curator. Your job is to prepare high quality data for others to use. A lot of work happens behind the scenes in a museum.

In fact, the curator has zones just like a Data Lakehouse. They receive the museum pieces, then they decide which pieces to display, and lastly they put them in the museum for visitors to enjoy. Many pieces are in storage because it isn't time for them to be on display.

How will you decide which data should appear for others to use?

### Curated Data Attributes

-   High quality
-   Filtered for privacy
-   Can be a composition of multiple data sources

We can **join** multiple trusted data sources, and apply other transformations to create curated data.

