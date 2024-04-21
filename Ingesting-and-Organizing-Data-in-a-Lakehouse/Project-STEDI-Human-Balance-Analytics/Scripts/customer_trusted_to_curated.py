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

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1713704579173 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_trusted", transformation_ctx="AccelerometerTrusted_node1713704579173")

# Script generated for node Customer Trusted
CustomerTrusted_node1713704560146 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_trusted", transformation_ctx="CustomerTrusted_node1713704560146")

# Script generated for node SQL Query
SqlQuery0 = '''
select distinct
serialnumber
,sharewithpublicasofdate
,birthday
,registrationdate
,sharewithresearchasofdate
,customername
,email
,lastupdatedate
,phone
,sharewithfriendsasofdate
from at inner join ct on 
at.user = ct.email
'''
SQLQuery_node1713704867594 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"al":AccelerometerTrusted_node1713704579173, "ct":CustomerTrusted_node1713704560146}, transformation_ctx = "SQLQuery_node1713704867594")

# Script generated for node Customer Curated
CustomerCurated_node1713705383772 = glueContext.getSink(path="s3://geh-stedi/customer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="CustomerCurated_node1713705383772")
CustomerCurated_node1713705383772.setCatalogInfo(catalogDatabase="stedi",catalogTableName="customer_curated")
CustomerCurated_node1713705383772.setFormat("json")
CustomerCurated_node1713705383772.writeFrame(SQLQuery_node1713704867594)
job.commit()