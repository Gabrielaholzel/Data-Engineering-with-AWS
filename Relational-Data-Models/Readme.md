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
