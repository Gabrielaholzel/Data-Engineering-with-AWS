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
