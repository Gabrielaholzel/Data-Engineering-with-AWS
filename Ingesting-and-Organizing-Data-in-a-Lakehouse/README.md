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

**"As a last step, the processing layer curates a trusted zone dataset by modeling it and joining it with other datasets, and stores it in curated layer."**

"Typically, datasets from the curated layer are partly or fully ingested into Amazon Redshift data warehouse storage to serve use cases that need very low latency access or need to run complex SQL queries."

Source:  [(opens in a new tab)](https://aws.amazon.com/blogs/big-data/build-a-lake-house-architecture-on-aws/)[https://aws.amazon.com/blogs/big-data/build-a-lake-house-architecture-on-aws/(opens in a new tab)](https://aws.amazon.com/blogs/big-data/build-a-lake-house-architecture-on-aws/)

### Structure and Format

Because querying and reading data from S3 is billed by the gigabyte, optimizing those queries is a very good idea. Data can be compressed at a very high ratio, using  **gzip**  and other compression formats. Whenever possible, data in S3 should also be in a columnar format like  **parquet**  files. This means that when issuing queries to S3, the entire row of data doesn't need to be scanned to locate a single field. The query becomes more efficient and cheaper.
