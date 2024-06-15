from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                 redshift_conn_id="",
                 sql_query="",
                 table="",
                 truncate_param = False,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        # self.conn_id = conn_id
        self.redshift_conn_id = redshift_conn_id
        self.sql_query = sql_query
        self.table = table
        self.truncate_param = truncate_param

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        try:
            if self.truncate_param:
                self.log.info("Truncating table {}".format(self.table))
                redshift.run("TRUNCATE TABLE {}".format(self.table))
            
            self.log.info("Loading data to {}".format(self.table))
            redshift.run("INSERT INTO {} {}".format(self.table, self.sql_query))
            self.log.info("Data has been copied successfully")
            
        except Exception as e:
            self.log.info("The copy has failed with the following error: {}".format(e))