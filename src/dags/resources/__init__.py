import os

from dagster import ResourceDefinition
from dagster_aws.s3 import s3_resource
from dagster_pyspark import pyspark_resource

from .postgres_io_manager import postgres_io_manager
from .api_clients.onyx_api_scraper import OnyxScraper, OnyxMockScraper, onyx_api_client, onyx_mock_api_client
from .schedules import daily_partitioned_config


postgres_io_manager_prod = postgres_io_manager.configured({
    "database": "coffee_belt"
})

RESOURCES_PROD = {
    "warehouse_io_manager": postgres_io_manager_prod,
    "warehouse_loader": postgres_io_manager_prod,
    # "postgres": configured_postgres,
    # "pyspark": configured_pyspark,
}
