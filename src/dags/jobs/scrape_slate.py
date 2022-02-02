from mock import patch

from dags.ops.product_scraping import get_product_list, get_product_info, process_product_collection
from dags.resources import (
    RESOURCES_PROD,
    slate_api_client,
    slate_mock_api_client,
    daily_partitioned_config,
)
from datetime import datetime
from dagster import (
    ResourceDefinition,
    graph,
    in_process_executor,
)

@graph
def get_active_products():
    product_list = get_product_list().map(get_product_info)
    product_df = process_product_collection(product_list.collect())
    return product_df

scrape_slate_prod = get_active_products.to_job(
    resource_defs={
        **{
            "api_client": slate_api_client,
            "partition_bounds": ResourceDefinition.none_resource(),
        },
        **RESOURCES_PROD,
    },
    config=daily_partitioned_config,
)

scrape_slate_test = get_active_products.to_job(
    resource_defs={
        **{
            "api_client": slate_mock_api_client,
            "partition_bounds": ResourceDefinition.none_resource(),
        },
        **RESOURCES_PROD,
    },
    config=daily_partitioned_config,
)
