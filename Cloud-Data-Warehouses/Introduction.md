# Introduction to Data Warehouses

## Introduction to Data Warehouses

The data warehouse plays a crucial role in the modern enterprise, storing and serving data for data visualization, analytics, and machine learning applications. As a data engineer, you likely will be tasked with designing and building these important data platforms.

![Diagram of a data warehouse solution](https://video.udacity-data.com/topher/2022/November/6376f33e_l1-introduction-to-cloud-data-warehouses/l1-introduction-to-cloud-data-warehouses.jpg)

A data warehouse is a system including processes, technologies & data representations that enables us to support analytical processes.

### Operational vs Analytical Business Processes

**Operational processes:**  Make it work.

-   Find goods & make orders (for customers)
-   Stock and find goods (for inventory staff)
-   Pick up & deliver goods (for delivery staff)

**Analytical processes:**  What is going on?

-   Assess the performance of sales staff (for HR)
-   See the effect of different sales channels (for marketing)
-   Monitor sales growth (for management)

![Data Warehouse is a system that enables us to support analytical processes](https://video.udacity-data.com/topher/2021/August/6111bc21_l1-introduction-to-datawarehousing/l1-introduction-to-datawarehousing.png)

Data Warehouse is a system that enables us to support analytical processes

## Data Warehouse Architecture

> A data warehouse is a copy of transaction data specifically structured for query and analysis. -  _Kimball_

> A data warehouse is a subject-oriented, integrated, nonvolatile, and time-variant collection of data in support of management's decisions. -  _Inmon_

> A data warehouse is a system that retrieves and consolidates data periodically from the source systems into a dimensional or normalized data store. It usually keeps years of history and is queried for business intelligence or other analytical activities. It is typically updated in batches, not every time a transaction happens in the source system. -  _Rainard_


### Data Warehouse: Technical Perspective

Extract the data from the source systems used for operations, transform the data, and load it into a dimensional model

![Kimball's Bus architecture](https://video.udacity-data.com/topher/2021/August/6112ddd2_l1-introduction-to-datawarehousing-3/l1-introduction-to-datawarehousing-3.png)

Kimball's Bus architecture

![The dimensional model of a data warehouse makes it easy for business users to work with the data and improves analytical query performance](https://video.udacity-data.com/topher/2021/August/6111d21c_l1-introduction-to-datawarehousing-1/l1-introduction-to-datawarehousing-1.png)

The Dimensional Model of a Data Warehouse

Business-user-facing application are needed, with clear visuals - Business Intelligence (BI) apps

### ETL: A Closer Look

Extracting:

-   Transfer data to the warehouse

Transforming:

-   Integrates many sources together
-   Possibly cleansing: inconsistencies, duplication, missing values, etc..
-   Possibly producing diagnostic metadata

Loading:

-   Structuring and loading the data into the dimensional data model


### Dimensional Model Review

**Goals of the Star Schema**

-   Easy to understand
-   Fast analytical query performance

**Fact Tables**

-   Record business events, like an order, a phone call, a book review
-   Fact tables columns record events recorded in quantifiable metrics like quantity of an item, duration of a call, a book rating

**Dimension Tables**

-   Record the context of the business events, e.g. who, what, where, why, etc..
-   Dimension tables columns contain attributes like the store at which an item is purchased or the customer who made the call, etc.

  

### ETL: A Closer Look

**Extracting:**

-   Transfer data to the warehouse

**Transforming:**

-   Integrates many sources together
-   Possibly cleansing: inconsistencies, duplication, missing values, etc..
-   Possibly producing diagnostic metadata

**Loading:**

-   Structuring and loading the data into the dimensional data model

### Example: The DVD Rentals Sample Database

![The Star Schema is easier for business users to understand versus Third Normal Form Schema ](https://video.udacity-data.com/topher/2021/August/6111d490_l1-introduction-to-datawarehousing-2/l1-introduction-to-datawarehousing-2.png)

Third Normal Form Schema VS Star Schema

### Naive Extract Transform and Load (ETL): From Third Normal Form to ETL

**Extract**

-   Query the 3NF DB

**Transform**

-   Join tables together
-   Change types
-   Add new columns

**Load**

-   Insert into facts & dimension tables
