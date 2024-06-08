# Introduction

## Project: Data Modeling with Cassandra

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

They'd like a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions, and wish to bring you on the project. My role was to create a database for this analysis. 

## Project Overview

In this project, I applied what I've learned on data modeling with Apache Cassandra and complete an ETL pipeline using Python. To complete the project, I needed to model the data by creating tables in Apache Cassandra to run queries. 

# Project Details

## Datasets

For this project, I worked with one dataset:  `event_data`. The directory of CSV files partitioned by date. Here are examples of filepaths to two files in the dataset:

```python
event_data/2018-11-08-events.csv 
event_data/2018-11-09-events.csv
```

## Project Steps

Below are steps I followed to complete each component of this project.

#### Modeling the NoSQL database or Apache Cassandra database

1.  Designed tables to answer the queries outlined in the project template.
2.  Wrote Apache Cassandra  `CREATE KEYSPACE`  and  `SET KEYSPACE`  statements.
3.  Developed the  `CREATE`  statement for each of the tables to address each question.
4.  Loaded the data with  `INSERT`  statement for each of the tables.
5.  Included  `IF NOT EXISTS`  clauses in the  `CREATE`  statements to create tables only if the tables do not already exist. I also included  `DROP TABLE`  statements for each table, so that I could run drop and create tables whenever I wanted to reset your database and test the ETL pipeline.
6.  Tested by running the proper select statements with the correct  `WHERE`  clause.

#### Building the ETL Pipeline

1.  Implemented the logic in section Part I of the notebook template to iterate through each event file in  `event_data`  to process and create a new CSV file in Python.
2.  Made necessary edits to Part II of the notebook template to include Apache Cassandra  `CREATE`  and  `INSERT`  statements to load processed records into relevant tables in the data model.
3.  Tested by running  `SELECT`  statements after running the queries on the database.
