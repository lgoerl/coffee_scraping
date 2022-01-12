from dags.ops.product_scraping import get_product_list, get_product_info, process_product_collection
from datetime import datetime
from dagster import graph, daily_partitioned_config, in_process_executor

@graph
def get_active_products():
    product_list = get_product_list()

    products = product_list.map(get_product_info)
    product_df = process_product_collection(products.collect())

    products = []
    for product in product_list:
        products.append(get_product_info(product))
    return products

scrape_onyx_prod = get_active_products.to_job(
    resource_defs={
        **{
            "api_client": onyx_api_client,
        },
        **RESOURCES_PROD,
    },
    tags=DOWNLOAD_TAGS,
    config=daily_download_config,
)


# scrape_onyx_staging = get_active_products.to_job(
#     resource_defs={
#         **{
#             "partition_bounds": partition_bounds,
#             "api_client": hn_api_subsample_client.configured({"sample_rate": 10}),
#         },
#         **RESOURCES_STAGING,
#     },
#     tags=DOWNLOAD_TAGS,
#     config=daily_download_config,
# )

scrape_onyx_test = get_active_products.to_job(
    resource_defs={
        **{
            "api_client": onyx_mock_api_client
        },
        **RESOURCES_LOCAL,
    },
    config={
        "resources": {
            "partition_bounds": {
                "config": {
                    "start": "2020-12-30 00:00:00",
                    "end": "2020-12-30 01:00:00",
                }
            },
        }
    },
    executor_def=in_process_executor,
)