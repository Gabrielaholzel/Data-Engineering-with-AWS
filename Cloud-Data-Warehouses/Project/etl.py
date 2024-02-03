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


def main():
    try:
        config = configparser.ConfigParser()
        config.read('dwh.cfg')
    
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        cur = conn.cursor()
        
        load_staging_tables(cur, conn)
        insert_tables(cur, conn)
    
        conn.close()
    except Error as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
