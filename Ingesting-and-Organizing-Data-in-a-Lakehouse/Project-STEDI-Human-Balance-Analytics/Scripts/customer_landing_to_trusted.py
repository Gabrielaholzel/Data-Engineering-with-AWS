import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Customer Landing
CustomerLanding_node1713700316647 = glueContext.create_dynamic_frame.from_options(format_options={"multiline": True}, connection_type="s3", format="json", connection_options={"paths": ["s3://geh-stedi/customer/landing/"], "recurse": True}, transformation_ctx="CustomerLanding_node1713700316647")

# Script generated for node SQL Query
SqlQuery3226 = '''
select * from myDataSource
where 
sharewithresearchasofdate is not null
'''
SQLQuery_node1713703174555 = sparkSqlQuery(glueContext, query = SqlQuery3226, mapping = {"myDataSource":CustomerLanding_node1713700316647}, transformation_ctx = "SQLQuery_node1713703174555")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1713702615057 = glueContext.write_dynamic_frame.from_catalog(frame=SQLQuery_node1713703174555, database="stedi", table_name="customer_trusted", additional_options={"enableUpdateCatalog": True, "updateBehavior": "UPDATE_IN_DATABASE"}, transformation_ctx="AWSGlueDataCatalog_node1713702615057")

job.commit()