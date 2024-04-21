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

# Script generated for node Customer Trusted
CustomerTrusted_node1713703642712 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_trusted", transformation_ctx="CustomerTrusted_node1713703642712")

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1713703546380 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_landing", transformation_ctx="AccelerometerLanding_node1713703546380")

# Script generated for node Join
Join_node1713703666104 = Join.apply(frame1=AccelerometerLanding_node1713703546380, frame2=CustomerTrusted_node1713703642712, keys1=["user"], keys2=["email"], transformation_ctx="Join_node1713703666104")

# Script generated for node SQL Query
SqlQuery4562 = '''
select distinct timestamp,user,x,y,z from myDataSource
'''
SQLQuery_node1713706019433 = sparkSqlQuery(glueContext, query = SqlQuery4562, mapping = {"myDataSource":Join_node1713703666104}, transformation_ctx = "SQLQuery_node1713706019433")

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1713703887711 = glueContext.getSink(path="s3://geh-stedi/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AccelerometerTrusted_node1713703887711")
AccelerometerTrusted_node1713703887711.setCatalogInfo(catalogDatabase="stedi",catalogTableName="accelerometer_trusted")
AccelerometerTrusted_node1713703887711.setFormat("json")
AccelerometerTrusted_node1713703887711.writeFrame(SQLQuery_node1713706019433)
job.commit()