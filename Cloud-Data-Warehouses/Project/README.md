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
   git clone https://github.com/your-username/Sparkify-Data-Warehouse.git

2. **Configure AWS Credentials**:

Ensure your AWS credentials are correctly set up in the .aws folder.

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

![Database Schema](Cloud-Data-Warehouses/Project/database-schema.jpg)
