from datetime import datetime, timedelta
import pendulum
import os
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from final_project_operators.stage_redshift import StageToRedshiftOperator
from final_project_operators.load_fact import LoadFactOperator
from final_project_operators.load_dimension import LoadDimensionOperator
from final_project_operators.data_quality import DataQualityOperator
from udacity.common.final_project_sql_statements import SqlQueries # Slightly changed to improve readability


default_args = {
    'catchup': False,
    'depends_on_past': False,
    'email_on_retry': False,
    'owner': 'Gabriela',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': pendulum.now()
}

s3_bucket = 'geh-bucket'
s3_songs_key = 'song-data/A/A/'
s3_events_key = 'log-data'
log_json_file = 'log_json_path.json'
redshift_conn_id = 'redshift'
aws_credentials_id = 'aws_credentials'

@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)

def final_project():

    start_operator = DummyOperator(task_id='Begin_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        aws_credentials_id = aws_credentials_id,
        log_json_file = log_json_file,
        redshift_conn_id = redshift_conn_id,
        s3_bucket = s3_bucket,
        s3_key = s3_events_key,
        table = 'staging_events'
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        aws_credentials_id = aws_credentials_id,
        redshift_conn_id = redshift_conn_id,
        s3_bucket = s3_bucket,
        s3_key = s3_songs_key,
        table = 'staging_songs'
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id = redshift_conn_id,
        sql_query = SqlQueries.songplay_table_insert,
        table = 'songplays'
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id = redshift_conn_id,
        sql_query = SqlQueries.user_table_insert,
        table = 'users',
        truncate_param = True
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id = redshift_conn_id,
        sql_query = SqlQueries.song_table_insert,
        table = 'songs',
        truncate_param = True
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id = redshift_conn_id,
        sql_query = SqlQueries.artist_table_insert,
        table = 'artists',
        truncate_param = True
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id = redshift_conn_id,
        sql_query = SqlQueries.time_table_insert,
        table = 'time',
        truncate_param = True
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id = redshift_conn_id,
        tables = ['users', 'songs', 'artists', 'time']
    )

    end_operator = DummyOperator(task_id='End_execution')

    start_operator \
        >> [stage_events_to_redshift,stage_songs_to_redshift] \
            >> load_songplays_table \
                >> [load_song_dimension_table,load_user_dimension_table,load_artist_dimension_table, load_time_dimension_table] \
                    >> run_quality_checks \
                        >> end_operator



final_project_dag = final_project()