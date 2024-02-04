import configparser
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import cursor, connection
from sql_queries import copy_table_queries, insert_table_queries


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
        cur.execute(query)
        conn.commit()


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
        cur.execute(query)
        conn.commit()

def read_config(file_path='dwh.cfg' : str):
    """
    Reads configuration file.

    Args:
    file_path: String path to the configuration file.

    Returns:
    config['CLUSTER'].values(): String elements of the config['CLUSTER'] dict. 
        They are strings for: host, database name, user, password and port.
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['CLUSTER'].values()

def main():
    host, dbname, user, password, port = read_config()
    with psycopg2.connect(f"host={host} dbname={dbname} user={user} password={password} port={port}") as conn:
        with conn.cursor() as cur:
            load_staging_tables(cur, conn)
            insert_tables(cur, conn)

if __name__ == "__main__":
    main()
