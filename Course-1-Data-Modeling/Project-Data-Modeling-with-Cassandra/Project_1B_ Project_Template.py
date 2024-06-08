#!/usr/bin/env python
# coding: utf-8

# # Part I. ETL Pipeline for Pre-Processing the Files

# ## PLEASE RUN THE FOLLOWING CODE FOR PRE-PROCESSING THE FILES

# #### Import Python packages 

# In[1]:


import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv


# #### Creating list of filepaths to process original event csv data files
# To do this, we first check if we are working in the right directory. 

# In[2]:


os.getcwd()


# Now we get our current folder and subfolder event data. Next, we create a for loop to create a list of files and collect each filepath. In said for, we join the file path and roots with the subdirectories using a glob.

# In[3]:


filepath = os.getcwd() + '/event_data'

for root, dirs, files in os.walk(filepath):
    file_path_list = glob.glob(os.path.join(root,'*'))


# #### Processing the files to create the data file csv that will be used for Apache Casssandra tables

# To process the files, we initiate an empty list. In this list, we append each data row by row. To achieve this, we create a for loop iterating over the list of files that we've generated. Within each iteration, we read the CSV file using a `reader` object and extract the data.

# In[4]:


full_data_rows_list = [] 
    
for f in file_path_list:
    with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
        csvreader = csv.reader(csvfile) 
        next(csvreader)
        
        for line in csvreader:
            full_data_rows_list.append(line) 


# We create a smaller event data csv file called `event_datafile_full.csv` that will be used to insert data into the Apache Cassandra tables.

# In[5]:


csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
    writer = csv.writer(f, dialect='myDialect')
    writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',                'level','location','sessionId','song','userId'])
    for row in full_data_rows_list:
        if (row[0] == ''):
            continue
        writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))


# #### Checking the structures we will be working with
# We start by getting total number of rows.

# In[6]:


len(full_data_rows_list)


# Next, checking the first element to see what the list of event data rows will look like. We can see that every element is a string, so we will need to change it to the appropriate format in the future.

# In[7]:


full_data_rows_list[0]


# Lastly, checking the number of rows in the smaller csv file.

# In[8]:


with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
    print(sum(1 for line in f))


# # Part II. Complete the Apache Cassandra coding portion of your project. 
# 
# ## Now you are ready to work with the CSV file titled <font color=red>event_datafile_new.csv</font>, located within the Workspace directory.  The event_datafile_new.csv contains the following columns: 
# - artist 
# - firstName of user
# - gender of user
# - item number in session
# - last name of user
# - length of the song
# - level (paid or free song)
# - location of the user
# - sessionId
# - song title
# - userId
# 
# The image below is a screenshot of what the denormalized data should appear like in the <font color=red>**event_datafile_new.csv**</font> after the code above is run:<br>
# 
# <img src="images/image_event_datafile_new.jpg">

# # Starting the Project
# To begin the ETL, we need to complete the set up to the Cassandra database. This is a three-step process, consisting of the following:

# #### 1. Creating a Cluster
# This connects to our local instance of Apache Cassandra. This connection will reach out to the database and insure we have the correct privileges to connect to this database. Once we get back the cluster object, we need to connect to it and that will create our session that we will use to execute queries.

# In[9]:


from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect()


# #### 2. Creating a Keyspace
# The Keyspace is like our database. We need to create it first to be able to create our tables. 

# In[10]:


try:
    session.execute("""
                    CREATE KEYSPACE IF NOT EXISTS udacity
                    WITH REPLICATION = 
                    {'class' : 'SimpleStrategy', 'replication_factor': 1}
                    """
                   )
except Exception as e:
    print(e)


# #### 3. Set Keyspace
# We set the Keyspace created as the database that we will be using. 

# In[11]:


try:
    session.set_keyspace('udacity')
except Exception as e:
    print(e)


# ## Instructions: 
# Create queries to ask the following three questions of the data.
# 
# ### 1. Get the artist, song title and song's length in the music app history that was heard during  sessionId = 338, and itemInSession  = 4

# To do this, we create a table called `session_history`. Since we will be filtering based on the `session_id` and `item_in_session`, we include both columns as we will use them as our `PRIMARY KEY`s. Furthermore, we need to get the `artist_name`, `song_title` and `song_length`, so we will also include these columns. <u>We should always keep in mind that we model the database tables on the queries we want to run</u>.
# 
# Moreover, we add an execution of the query `DROP TABLE IF EXISTS` before the creation query, to be able to modify the create query easily. 

# In[12]:


session_history_create = "CREATE TABLE IF NOT EXISTS session_history "
session_history_create += "(                            session_id int,                             item_in_session int,                             artist_name text,                             song_title text,                             song_length float,                             PRIMARY KEY (session_id, item_in_session)                             )"

try:
    session.execute("DROP TABLE IF EXISTS session_history")
    session.execute(session_history_create)
except Exception as e:
    print(e)  


# Next, we read the file with a `reader` object (skipping the header), to insert the values read into the created table. To do this, we select which column element will be assigned for each column in the `INSERT` statement. For example, the first column of the table is `session_id`, which correspond with `line[8]` in our CSV file. Moreover, every element is a string, so we change it accordingly for the non-text columns.

# In[13]:


file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) 
    for line in csvreader:
        query = "INSERT INTO session_history (session_id, item_in_session, artist_name, song_title, song_length)"
        query = query + "VALUES (%s, %s, %s, %s, %s)"
        session.execute(query, (int(line[8]), int(line[3]), line[0], line[9], round(float(line[5]),2)))


# As to retreive the information requested, we perform a `SELECT` statement with the appropriate `WHERE` clause.
# 
# We can see that during `session_id = 338` and `item_in_session = 4`, the artist that was heard was *Faithless*, the song's name is *Music Matters (Mark Knight Dub)* and the length of the song is of *495.31*.

# In[14]:


try:
    rows = session.execute("SELECT                                 artist_name,                                 song_title,                                 song_length                             FROM                                 session_history                             WHERE                                 session_id = 338                                 AND item_in_session = 4")
except Exception as e:
    print(e)  

for row in rows:
    print(row.artist_name, row.song_title, row.song_length)


# ### 2. Get the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
# This time, we create a table called `user_artist_history`. Since we will be filtering based on the `user_id` and `session_id`, we include both columns as we will use them as our `PRIMARY KEY`s. We also include the column `item_in_session` as a clustered column for sorting purposes. 
# 
# Furthermore, we need to get the `artist_name`, `song_title`, `user_first` (for the user's first name) and `user_last` (for the user's last name), so we will also include these columns. 
# 
# Once again, we add an execution of the query `DROP TABLE IF EXISTS` before the creation query, to be able to modify the create query easily. 

# In[15]:


user_artist_history_create = "CREATE TABLE IF NOT EXISTS user_artist_history "
user_artist_history_create += "(                            user_id int,                             session_id int,                             item_in_session int,                             artist_name text,                             song_title text,                             user_first text,                             user_last text,                             PRIMARY KEY ((user_id, session_id), item_in_session)                             )"
try:
    session.execute("DROP TABLE IF EXISTS user_artist_history")
    session.execute(user_artist_history_create)
except Exception as e:
    print(e)            


# Once more, we execute the `INSERT INTO` statement the same way as we did with the previous table.

# In[16]:


with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) 
    for line in csvreader:
        query = "INSERT INTO user_artist_history (                                                  user_id,                                                   session_id,                                                   item_in_session,                                                   artist_name,                                                   song_title,                                                   user_first,                                                   user_last)"
        query = query + "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        session.execute(query, (int(line[10]), int(line[8]), int(line[3]), line[0], line[9], line[1], line[4]))


# Finally, we execute the `SELECT` statement to retreive the information inquired with the appropriate `WHERE` clause.
# 
# We can observe that the user *Sylvie Cruz*, corresponding to the `user_id = 10`, has listened to four songs from different artists during `session_id = 182`.

# In[17]:


try:
    rows = session.execute("SELECT                                 artist_name,                                 song_title,                                 user_first,                                 user_last                             FROM                                 user_artist_history                             WHERE                                 user_id = 10                                 AND session_id = 182")
except Exception as e:
    print(e)  

for row in rows:
    print(row.artist_name, row.song_title, row.user_first, row.user_last)


# ### 3. Get every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
# 
# For this last activity, we create a table called `user_history`. Again, we will be filtering based on the `song_title`, so we include this column as well to use it as one of our `PRIMARY KEY`s. We also include the column `user_id` as a `PRIMARY KEY`, since many users can listen to the same song, and we will need to store all of these records in our table.
# 
# Furthermore, we need to get the `user_first` and `user_last`, so we will also include these columns. 
# 
# Once again, we add an execution of the query `DROP TABLE IF EXISTS` before the creation query, to be able to modify the create query easily. 

# In[18]:


user_history_create = "CREATE TABLE IF NOT EXISTS user_history "
user_history_create += "(                            song_title text,                             user_id int,                             user_first text,                             user_last text,                             PRIMARY KEY (song_title, user_id)                             )"
try:
    session.execute("DROP TABLE IF EXISTS user_history")
    session.execute(user_history_create)
except Exception as e:
    print(e)          


# Finally, we execute the appropriate `INSERT INTO` statement.

# In[19]:


with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) 
    for line in csvreader:
        query = "INSERT INTO user_history (                                           song_title,                                            user_id,                                            user_first,                                            user_last)"
        query = query + "VALUES (%s, %s, %s, %s)"
        session.execute(query, (line[9], int(line[10]), line[1], line[4]))


# And we get the information requested using an `SELECT` statement with the suitable `WHERE` clause. We can see that there were three users that have heard this song.

# In[20]:


try:
    rows = session.execute("SELECT                                 user_first,                                 user_last                             FROM                                 user_history                             WHERE                                 song_title = 'All Hands Against His Own'")
except Exception as e:
    print(e)  

for row in rows:
    print(row.user_first, row.user_last)


# ### Cleaning

# To clear the space, we drop the three tables created and close out the sessions. We do this using a for loop with a `DROP TABLE` query iterating over the tables created. 

# In[21]:


tables = ['session_history', 'user_artist_history', 'user_history']

try:
    for table in tables:
        session.execute("DROP TABLE IF EXISTS " + table)
except Exception as e:
    print(e)


# We shut down the session as well as the cluster.

# In[22]:


session.shutdown()
cluster.shutdown()

