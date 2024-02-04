import configparser
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import cursor, connection
from sql_queries import copy_table_queries, insert_table_queries
from typing import ValuesView


def load_staging_tables(cur: cursor, conn: connection) -> None:
    """
    Load data from S3 into staging tables on Redshift.

    Args:
    cur: Cursor object for the database connection.
    conn: Connection object to the Redshift database.

    Returns:
    None
    """
    for query in copy_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            conn.rollback()


def insert_tables(cur: cursor, conn: connection) -> None:
    """
    Inserts data into target tables.

    Args:
    cur: Cursor object for the database connection.
    conn: Connection object to the Redshift database.

    Returns:
    None
    """
    for query in insert_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except Exception as e:
            print(f"Error executing query: {e}")
            conn.rollback()
            
def validate_queries(cur: cursor) -> None:
    """
    Validates that the tables have been correctly loaded.

    Args:
    cur: Cursor object for the database connection.

    Returns:
    None
    """
    try:
        print("The number of records in the songplays table is: ")
        sp_count = cur.execute("SELECT COUNT(*) FROM songplays;")
        sp_count.fetchone()
        
        print("The duplicate records in the songplays table are: ")
        dup_records = cur.execute("SELECT COUNT(*), start_time, user_id, song_id, artist_id \
                                   FROM songplays \
                                   GROUP BY start_time, user_id, song_id, artist_id \
                                   HAVING COUNT(*) > 1;")
        sp_count.fetchall()
    
    except Exception as e:
        print(f"Error executing query: {e}")
        conn.rollback()
    

def read_config(file_path: str = 'dwh.cfg') -> ValuesView:
    """
    Reads configuration file.

    Args:
    file_path: String path to the configuration file.

    Returns:
    config['CLUSTER'].values(): dict_values object containing the following: host, database name, user, password and port.
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['CLUSTER'].values()

def main():
    """
    Reads configuration parameters from config file. 
    Executes load_staging_tables for loading staging tables from S3 files.
    Executes insert_tables to insert staging data into tables in DB.

    Args:
    None

    Returns:
    None
    """
    host, dbname, user, password, port = read_config()
    with psycopg2.connect(f"host={host} dbname={dbname} user={user} password={password} port={port}") as conn:
        with conn.cursor() as cur:
            load_staging_tables(cur, conn)
            insert_tables(cur, conn)
            validate_queries(cur)

if __name__ == "__main__":
    main()
