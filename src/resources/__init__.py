import os

from dagster import ResourceDefinition
from dagster_aws.s3 import s3_resource
from dagster_pyspark import pyspark_resource

from .postgres_io_manager import postgres_io_manager

# configured_pyspark = pyspark_resource.configured(
#     {
#         "spark_conf": {
#             "spark.jars.packages": ",".join(
#                 [
#                     "net.snowflake:snowflake-jdbc:3.8.0",
#                     "net.snowflake:spark-snowflake_2.12:2.8.2-spark_3.0",
#                     "com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.7",
#                 ]
#             ),
#             "spark.hadoop.fs.s3.impl": "org.apache.hadoop.fs.s3native.NativeS3FileSystem",
#             "spark.hadoop.fs.s3.awsAccessKeyId": os.getenv("AWS_ACCESS_KEY_ID", ""),
#             "spark.hadoop.fs.s3.awsSecretAccessKey": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
#             "spark.hadoop.fs.s3.buffer.dir": "/tmp",
#         }
#     }
# )


postgres_io_manager_prod = postgres_io_manager.configured({
    "database": "STG_COFFEES"
})

RESOURCES_PROD = {
    "warehouse_io_manager": postgres_io_manager_prod,
    "warehouse_loader": postgres_io_manager_prod,
    "postgres": configured_postgres,
    # "pyspark": configured_pyspark,
}