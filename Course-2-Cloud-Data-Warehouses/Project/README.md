# Sparkify Data Warehouse Project

## Overview

This project involves building an ETL (Extract, Transform, Load) pipeline for a music streaming startup called Sparkify. The goal is to move their user and song data, currently residing in S3, into a Redshift data warehouse. The data engineering tasks include creating tables, staging data, and transforming it into dimensional tables suitable for analytics.

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Table Descriptions](#table-descriptions)
- [Example Queries](#example-queries)
- [Helpful Hints](#helpful-hints)
- [Acknowledgements](#acknowledgements)

## Project Structure

The project consists of several components:

- `create_tables.py`: Python script for creating the necessary tables in Redshift.
- `etl.py`: Python script for executing the ETL pipeline, extracting data from S3, staging it in Redshift, and transforming it into dimensional tables.
- `sql_queries.py`: SQL queries for creating tables, copying data, and transforming it.

## Getting Started

To set up the project, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Gabrielaholzel/Data-Engineering-with-AWS.git

2. **Configure AWS Credentials**:

Ensure your AWS credentials are correctly set up in the `dwh.cfg` file.

3. **Run the ETL Pipeline:**
   ```bash
   python create_tables.py
   python etl.py

## Table Descriptions

### `songplay` Table
* songplay_id: Unique identifier for each song play (primary key).
* start_time: Timestamp of when the song play started.
* user_id: ID of the user involved in the song play.
* level: User level (free or paid).
* song_id: ID of the song being played.
* artist_id: ID of the artist of the song.
* session_id: ID of the user's session.
* location: Location where the song play occurred.
* user_agent: User agent information.

### `users` Table
* user_id: User ID (primary key).
* first_name: User's first name.
* last_name: User's last name.
* gender: User's gender.
* level: User level (free or paid).

### `song` Table
* song_id: Song ID (primary key).
* title: Title of the song.
* artist_id: ID of the song's artist.
* year: Year the song was released.
* duration: Duration of the song in seconds.

### `artist` Table
* artist_id: Artist ID (primary key).
* name: Name of the artist.
* location: Location of the artist.
* latitude: Latitude of the artist's location.
* longitude: Longitude of the artist's location.

### `time` Table
* start_time: Timestamp (primary key).
* hour: Hour of the day.
* day: Day of the month.
* week: Week of the year.
* month: Month of the year.
* year: Year.
* weekday: Day of the week.

The database schema is as follows:

![Database Schema](https://github.com/Gabrielaholzel/Data-Engineering-with-AWS/blob/05f1f8e6bf124f30d2c2655fc55dde1095b37f19/Cloud-Data-Warehouses/Project/database-schema.jpg)



## Example Queries
Here are some example queries to gain insights into the Sparkify dataset:

1. Find the most popular songs
   ```sql
   SELECT s.title, COUNT(sp.songplay_id) AS play_count
   FROM songplay sp
      JOIN song s ON sp.song_id = s.song_id
   GROUP BY s.title
   ORDER BY play_count DESC
   LIMIT 10;

2. Explore user activity during different times of the day
   ```sql
   SELECT t.hour, COUNT(sp.songplay_id) AS play_count
   FROM songplay sp
   JOIN time t ON sp.start_time = t.start_time
   GROUP BY t.hour
   ORDER BY t.hour;
   
3. Identify the top users by the number of song plays
   ```sql
   SELECT u.user_id, u.first_name, u.last_name, COUNT(sp.songplay_id) AS play_count
   FROM songplay sp
   JOIN users u ON sp.user_id = u.user_id
   GROUP BY u.user_id, u.first_name, u.last_name
   ORDER BY play_count DESC
   LIMIT 10;


4. Discover the distribution of user levels
   ```sql
   SELECT level, COUNT(DISTINCT user_id) AS user_count
   FROM users
   GROUP BY level;

5. Find the most active locations
   ```sql
   SELECT location, COUNT(songplay_id) AS play_count
   FROM songplay
   GROUP BY location
   ORDER BY play_count DESC
   LIMIT 10;

6. Explore the most played songs in a specific month
   ```sql
   SELECT s.title, COUNT(sp.songplay_id) AS play_count
   FROM songplay sp
   JOIN song s ON sp.song_id = s.song_id
   JOIN time t ON sp.start_time = t.start_time
   WHERE t.month = 11 -- Replace with the desired month
   GROUP BY s.title
   ORDER BY play_count DESC
   LIMIT 10;

## Acknowledgements
This project is part of the Data Engineering Nanodegree at [Udacity](https://www.udacity.com/).
