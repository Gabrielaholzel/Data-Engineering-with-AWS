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

# Script generated for node SQL Join + Select
SqlQuery0 = '''
select timestamp, user, x,y,z 
from al join ct on al.user = ct.email
'''
SQLJoinSelect_node1713706546725 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"al":AccelerometerLanding_node1713703546380, "ct":CustomerTrusted_node1713703642712}, transformation_ctx = "SQLJoinSelect_node1713706546725")

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1713703887711 = glueContext.getSink(path="s3://geh-stedi/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AccelerometerTrusted_node1713703887711")
AccelerometerTrusted_node1713703887711.setCatalogInfo(catalogDatabase="stedi",catalogTableName="accelerometer_trusted")
AccelerometerTrusted_node1713703887711.setFormat("json")
AccelerometerTrusted_node1713703887711.writeFrame(SQLJoinSelect_node1713706546725)
job.commit()