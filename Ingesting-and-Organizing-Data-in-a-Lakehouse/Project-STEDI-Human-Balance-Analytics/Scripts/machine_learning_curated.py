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

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1713718930198 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_trusted", transformation_ctx="StepTrainerTrusted_node1713718930198")

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1713718978703 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_trusted", transformation_ctx="AccelerometerTrusted_node1713718978703")

# Script generated for node SQL Query
SqlQuery0 = '''
select distinct *
from stt 
    join at 
    on stt.sensorreadingtime = at.timestamp
'''
SQLQuery_node1713719016800 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"stt":StepTrainerTrusted_node1713718930198, "at":AccelerometerTrusted_node1713718978703}, transformation_ctx = "SQLQuery_node1713719016800")

# Script generated for node Machine Learning Curated
MachineLearningCurated_node1713719114149 = glueContext.getSink(path="s3://geh-stedi/step_trainer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="MachineLearningCurated_node1713719114149")
MachineLearningCurated_node1713719114149.setCatalogInfo(catalogDatabase="stedi",catalogTableName="machine_learning_curated")
MachineLearningCurated_node1713719114149.setFormat("json")
MachineLearningCurated_node1713719114149.writeFrame(SQLQuery_node1713719016800)
job.commit()