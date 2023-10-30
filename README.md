# Data Engineering with AWS

Welcome!

This repo is meant to be used as a notes bank for the [Data Engineering with AWS](https://www.udacity.com/course/data-engineer-nanodegree--nd027) nanodegree program by [Udacity](https://learn.udacity.com/).

---
## Introduction to Data Modeling
---
### What is Data Modeling?
> "... an abstraction that **organizes elements of data** and **how** they will **relate** to each other" -- Wikipedia

> "Data modeling is the **process of creating a visual representation** or a blueprint that defines the **information collection and management systems** of any organization. This blueprint or data model helps different stakeholders, like data analysts, scientists, and engineers, to create a unified view of the organization's data. The model **outlines what data the business collects, the relationship between different datasets, and the methods that will be used to store and analyze the data**." -- AWS

> "Data modeling is the **process of creating a visual representation** of either a whole information system or parts of it **to communicate connections** between data points and structures." -- IBM


Data modeling is a process to support both your business and your user applications. These two needs are particularly different. 

For example, let's say we owned an online store. We will need to store data so that we can understand how much stock we sold of a particular item. This is a business process, and we'll also need to store information about our customers as they'd log onto our website, a user application. 

* **Process to Support Business and Users Applications**
To begin a data modeling process, the team must gather requirements from the application team, the business users, and our end users to understand that data must be retained and served as a business or the end-users. 

* **Gather Requirements**
First, we need to map out that our data must be stored and persisted, and how that data will relate to each other. Next, we want to focus on conceptual data modeling. 

* **Conceptual Data Modeling**
The process of doing actual data modeling, starts with conceptual data modeling with entity mapping. This can be done actually by hand, or by using many tools to do this work. Conceptual data modeling is mapping the concepts of the data that you have or will have. 
According to [AWS](https://aws.amazon.com/what-is/data-modeling/), conceptual data models give a big picture view of data. They explain the following:
	* What data the system contains
	* Data attributes and conditions or constraints on the data
	* What business rules the data relates to
	* How the data is best organized
	* Security and data integrity requirements


* **Logical Data Modeling**
Logical data modeling is done where the contectual models are mapped to logical models using the concept of tables, schemas, and columns. According to [AWS](https://aws.amazon.com/what-is/data-modeling/), they give more details about the data concepts and complex data relationships that were identified in the conceptual data model, such as these:
	* Data types of the various attributes (for example, string or number)
	* Relationships between the data entities
	* Primary attributes or key fields in the data

Data architects and analysts work together to create the logical model. They follow one of several formal data modeling systems to create the representation. Sometimes agile teams might choose to skip this step and move from conceptual to physical models directly. However, these models are useful for designing large databases, called data warehouses, and for designing automatic reporting systems.




* **Physical Data Modeling**
Physical data modeling is done transforming the logical data modeling to the database's *Data Definition Language*, or **DDL** to be able to create the databases, the tables and the schemas. According to [AWS](https://aws.amazon.com/what-is/data-modeling/), physical data models map the logical data models to a specific DBMS technology and use the software's terminology. For example, they give details about the following:
	* Data field types as represented in the DBMS
	* Data relationships as represented in the DBMS
	* Additional details, such as performance tuning



---
### Why is Data Modeling Important?
---
According to [AWS](https://aws.amazon.com/what-is/data-modeling/), organizations today collect a large amount of data from many different sources. However, **raw data is not enough**. You need to *analyze data for actionable insights that can guide you to make profitable business decisions*. Accurate data analysis needs efficient **data collection, storage, and processing**. There are several database technologies and data processing tools, and different datasets require different tools for efficient analysis.

* **Data Organization:** The organization of the data for your applications is extremely important and makes everyone's life easier.
* **Use cases:** Having a well thought out and organized data model is critical to how that data can later be used. Queries that could have been straightforward and simple might become complicated queries if data modeling isn't well thought out.
* **Starting early:** Thinking and planning ahead will help you be successful. This is not something you want to leave until the last minute.
* **Iterative Process:** Data modeling is not a fixed process. It is iterative as new requirements and data are introduced. Having flexibility will help as new information becomes available.


---
## Introduction to Relational Databases
---

### Relational Model
This model **organizes data** into one or morte **tables** (or "relations") of **columns and rows**, with a **unique key* identifying each row. Generally, each table represents one "entity type" (such as customer or product).


![Relation](Images/relational-databases-relation.jpg)




















