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

# Script generated for node Customer Curated
CustomerCurated_node1713707577112 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_curated", transformation_ctx="CustomerCurated_node1713707577112")

# Script generated for node Step Trainer Landing
StepTrainerLanding_node1713707527087 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_landing", transformation_ctx="StepTrainerLanding_node1713707527087")

# Script generated for node SQL Join
SqlQuery4434 = '''
select sensorReadingTime
,stl.serialNumber
,distanceFromObject from stl inner join cc
on stl.serialnumber = cc.serialnumber
'''
SQLJoin_node1713707497925 = sparkSqlQuery(glueContext, query = SqlQuery4434, mapping = {"stl":StepTrainerLanding_node1713707527087, "cc":CustomerCurated_node1713707577112}, transformation_ctx = "SQLJoin_node1713707497925")

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1713709034163 = glueContext.write_dynamic_frame.from_catalog(frame=SQLJoin_node1713707497925, database="stedi", table_name="step_trainer_trusted", additional_options={"enableUpdateCatalog": True, "updateBehavior": "UPDATE_IN_DATABASE"}, transformation_ctx="StepTrainerTrusted_node1713709034163")

job.commit()