# Relational Data Models
## Databases

**Database:** A set of related data and the way it is organized.

**Database Management System:**  Computer software that allows users to interact with the database and provides access to all of the data.

The term database is often used to refer to both the database and the DBMS used.

  

**<u>Rule 1:</u> The information rule:**

All information in a relational database is represented explicitly at the logical level and in exactly one way – by values in tables.

### Importance of Relational Databases:

-   **Standardization of data model:**  Once your data is transformed into the rows and columns format, your data is standardized and you can query it with SQL
-   **Flexibility in adding and altering tables:**  Relational databases gives you flexibility to add tables, alter tables, add and remove data.
-   **Data Integrity:**  Data Integrity is the backbone of using a relational database.
-   **Structured Query Language (SQL):**  A standard language can be used to access the data with a predefined language.
-   **Simplicity :**  Data is systematically stored and modeled in tabular format.
-   **Intuitive Organization:**  The spreadsheet format in relational databases is intuitive for data modeling.

**Online Analytical Processing (OLAP):**

Databases optimized for these workloads allow for complex analytical and ad hoc queries, including aggregations. <u>These type of databases are optimized for reads</u>.

**Online Transactional Processing (OLTP):**

Databases optimized for these workloads allow for less complex queries in large volume. <u>The types of queries for these databases are read, insert, update, and delete</u>.

The key to remember the difference between OLAP and OLTP is analytics (A) vs transactions (T). If you want to get the price of a shoe then you are using OLTP (this has very little or no aggregations). If you want to know the total stock of shoes a particular store sold, then this requires using OLAP (since this will require aggregations).

#### Additional Resource on the difference between OLTP and OLAP:

This  [Stackoverflow post](https://stackoverflow.com/questions/21900185/what-are-oltp-and-olap-what-is-the-difference-between-them)  describes it well.


### Normalization and Denormalization

Normalization will feel like a natural process, you will reduce the number of copies of the data and increase the likelihood that your data is correct in all locations.

**Normalization** organizes the columns and tables in a database to ensure that their dependencies are properly enforced by database integrity constraints. We don’t want or need extra copies of our data, this is data redundancy. We want to be able to update data in one place and have that be the source of truth, that is data integrity.

**Denormalization** will not feel as natural, as you will have duplicate copies of data, and tables will be more focused on the queries that will be run.

Here is an example table we will be using later in our demo and exercises. Let’s say we have a table called music_library, looks pretty standard but this is not a normalized table.

![Relational data that is not normalized](https://video.udacity-data.com/topher/2021/August/612dd42e_use-this-version-data-modeling-lesson-2/use-this-version-data-modeling-lesson-2.png)

#### Objectives of Normal Form:

1.  To free the database from unwanted insertions, updates, & deletion dependencies
2.  To reduce the need for refactoring the database as new types of data are introduced
3.  To make the relational model more informative to users
4.  To make the database neutral to the query statistics

#### Process of Normalization
1.  **How to reach First Normal Form (1NF):** 
    -   Atomic values: each cell contains unique and single values  
    -   Be able to add data without altering tables  
    -   Separate different relations into different tables  
    -   Keep relationships between tables together with foreign keys

2.  **Second Normal Form (2NF):**  
    -   Have reached 1NF
    -   All columns in the table must rely on the Primary Key

3.  **Third Normal Form (3NF):**  
    -   Must be in 2nd Normal Form
    -   No transitive dependencies
    -   Remember, transitive dependencies you are trying to maintain is that to get from A-> C, you want to avoid going through B.

**When to use 3NF:**
When you want to update data, we want to be able to do in just 1 place. We want to avoid updating the table in the Customers Detail table (in the example in the lecture slide).

**Denormalization:**
The process of trying to improve the read performance of a database at the expense of losing some write performance by adding redundant copies of data.

JOINS on the database allow for outstanding flexibility but are extremely slow. If you are dealing with heavy reads on your database, you may want to think about denormalizing your tables. You get your data into normalized form, and then you proceed with denormalization. So, denormalization comes after normalization.

**Logical Design Change**
1. The Designer is in charge of keeping data consistent
2. Reads will be faster (select)
3. Writes will be slower (insert, update, delete)

# Denormalization Vs. Normalization

Let's take a moment to make sure you understand what was in the demo regarding denormalized vs. normalized data. These are important concepts, so make sure to spend some time reflecting on these.

**Normalization**  is about trying to increase data integrity by reducing the number of copies of the data. Data that needs to be added or updated will be done in as few places as possible.

**Denormalization**  is trying to increase performance by reducing the number of joins between tables (as joins can be slow). Data integrity will take a bit of a potential hit, as there will be more copies of the data (to reduce JOINS).

## Example of Denormalized Data:

As you saw in the earlier demo, this denormalized table contains a column with the Artist name that includes duplicated rows, and another column with a list of songs.

![](https://video.udacity-data.com/topher/2019/March/5c788517_table1/table1.png)

## Example of Normalized Data:

Now for normalized data, Amanda used 3NF. You see a few changes:  

1.  _No row contains a list of items._  For e.g., the list of song has been replaced with each song having its own row in the Song table.  
    
2.  _Transitive dependencies have been removed_. For e.g., album ID is the PRIMARY KEY for the album year in Album Table. Similarly, each of the other tables have a unique primary key that can identify the other values in the table (e.g., song id and song name within Song table).

#### Song_Table

![](https://video.udacity-data.com/topher/2019/March/5c797e7e_table4/table4.png)

#### Album_Table

![](https://video.udacity-data.com/topher/2019/March/5c797e87_table5/table5.png)

#### Artist_Table

![](https://video.udacity-data.com/topher/2019/March/5c797e8e_table6/table6.png)


## Fact and Dimension Tables
The following image shows the relationship between the fact and dimension tables for the example shown in the video. As you can see in the image, the unique primary key for each Dimension table is included in the Fact table.

**Dimension tables** categorise facts and measures in order to enable users to answer business questions. Dimensions are people, products, place and time.

In this example, it helps to think about the  **Dimension tables**  providing the following information:

-   **Where**  the product was bought? (Dim_Store table)
-   **When**  the product was bought? (Dim_Date table)
-   **What**  product was bought? (Dim_Product table)

The  **Fact table**  provides the  **metric of the business process**  (here Sales).

-   **How many**  units of products were bought? (Fact_Sales table)

![](https://video.udacity-data.com/topher/2019/March/5c81772b_dimension-fact-tables/dimension-fact-tables.png)

If you are familiar with  **Entity Relationship Diagrams**  (ERD), you will find the depiction of <u>STAR</u> and <u>SNOWFLAKE</u> schemas in the demo familiar. The ERDs show the data model in a concise way that is also easy to interpret. ERDs can be used for any data model, and are not confined to STAR or SNOWFLAKE schemas. Commonly available tools can be used to generate ERDs. However, more important than creating an ERD is to learn more about the data through conversations with the data team so as a data engineer you have a strong understanding of the data you are working with.

More information about ER diagrams can be found at this  [Wikipedia](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model)  page.

### Star Schemas
Star Schema is the simplest style of data mart schema. <u>The star schema consists of one of more fact tables referencing any number of dimension tables</u>.

-   Gets its name from the physical model resembling a star shape
-   A fact table is at its center
-   Dimension table surrounds the fact table representing the star’s points.

#### Additional Resources

Check out this Wikipedia page on  [Star schemas](https://en.wikipedia.org/wiki/Star_schema).


#### Benefits of Star Schema

-   **Denormalized:** Getting a table into 3NF is a lot of hard work, JOINs can be complex even on simple data
-   **Simplified queries:** Star schema allows for the relaxation of these rules and makes queries easier with simple JOINS
-   **Fast aggregations:** Aggregations perform calculations and clustering of our data so that we do not have to do that work in our application. Examples : COUNT, GROUP BY etc

#### Drawbacks of Star Schema
- **Issues with denormalization:** Issues like data integrity and decrease query flexibility. 
- **Data integrity:** You will have duplicated data spread across multiple tables. 
- **Decrease query flexibility:** When you denormalize tables, you are modeling to your query, so you won't be able to do as many ad-hoc queries on your tables. 
- **Many to many relationships simplified:** Star schemas only support one to one mappings. Many to many relationships are hard to support, and are abstracted away for sake of simplicity and to fit the model. 

Here you can see an example of a Star Schema:

![Music Store Database with Star Schema](https://video.udacity-data.com/topher/2021/August/612e9c72_use-this-version-data-modeling-lesson-2-1/use-this-version-data-modeling-lesson-2-1.png)


### Snowflake Schemas
It's a logical arrangement of tables in a multidimensional database represented by centralized fact tables which are connected to multiple dimensions. A complex snowflake shape emerges when the dimensions of a snowflake schema are elaborated, having multiple levels of relationships, child tables having multiple parents. 

**Snowflake vs Star Schema**
-   Star Schema is a special, simplified case of the snowflake schema.
-   Star schema does not allow for one to many relationships while the snowflake schema does.
-   Snowflake schema is more normalized than Star schema but only in 1NF or 2NF

# Data Definition and Constraints

## Data Definition and Constraints

The CREATE statement in SQL has a few important constraints that are highlighted below.

### NOT NULL

The  **NOT NULL**  constraint indicates that the column cannot contain a null value.

Here is the syntax for adding a NOT NULL constraint to the CREATE statement:

`CREATE TABLE IF NOT EXISTS customer_transactions (  
      customer_id int NOT NULL,
      store_id int,
      spent numeric
);` 

You can add  **NOT NULL**  constraints to more than one column. Usually this occurs when you have a  **COMPOSITE KEY**, which will be discussed further below.

Here is the syntax for it:

`CREATE TABLE IF NOT EXISTS customer_transactions (  customer_id int NOT NULL,  store_id int NOT NULL,     spent numeric
);` 

### UNIQUE

The  **UNIQUE**  constraint is used to specify that the data across all the rows in one column are unique within the table. The  **UNIQUE**  constraint can also be used for multiple columns, so that the combination of the values across those columns will be unique within the table. In this latter case, the values within 1 column do not need to be unique.  
  
Let's look at an example.

`CREATE TABLE IF NOT EXISTS customer_transactions (  customer_id int NOT NULL UNIQUE,  store_id int NOT NULL UNIQUE,     spent numeric 
);`

Another way to write a  **UNIQUE**  constraint is to add a table constraint using commas to separate the columns.

`CREATE TABLE IF NOT EXISTS customer_transactions (  customer_id int NOT NULL,  store_id int NOT NULL,  spent numeric,  UNIQUE (customer_id, store_id, spent)  );`

### PRIMARY KEY

The  **PRIMARY KEY**  constraint is defined on a single column, and every table should contain a primary key. The values in this column uniquely identify the rows in the table. If a group of columns are defined as a primary key, they are called a  **composite key**. That means the combination of values in these columns will uniquely identify the rows in the table. By default, the  **PRIMARY KEY**  constraint has the unique and not null constraint built into it.  
  
Let's look at the following example:

`CREATE TABLE IF NOT EXISTS store (  store_id int PRIMARY KEY,  store_location_city text,     store_location_state text
);`

Here is an example for a group of columns serving as  **composite key**.

`CREATE TABLE IF NOT EXISTS customer_transactions (  customer_id int,  store_id int,  spent numeric,  PRIMARY KEY (customer_id, store_id)  );`

To read more about these constraints, check out the  [PostgreSQL documentation](https://www.postgresql.org/docs/9.4/ddl-constraints.html).
