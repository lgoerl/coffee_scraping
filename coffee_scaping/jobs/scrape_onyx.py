import bs4 as beautiful_soup
import requests

from datetime import datetime
from dagster import graph, hourly_partitioned_config, in_process_executor

def get_product_list():
    pass

def get_product_info(product):
    pass

@graph
def get_active_products():
    pass

@daily_partitioned_config(start_date=datetime(2022, 1, 6))
def daily_download_config(start: datetime, end: datetime):
    return {
        "resources": {
            "partition_bounds": {
                "config": {
                    "start": start.strftime("%Y-%m-%d %H:%M:%S"),
                    "end": end.strftime("%Y-%m-%d %H:%M:%S"),
                }
            },
        }
    }

scrape_onyx_prod = get_active_produts.to_job(
    resource_defs={
        **{
            "partition_bounds": partition_bounds,
            "hn_client": hn_api_subsample_client.configured({"sample_rate": 10}),
        },
        **RESOURCES_PROD,
    },
    tags=DOWNLOAD_TAGS,
    config=hourly_download_config,
)


download_staging_job = hacker_news_api_download.to_job(
    resource_defs={
        **{
            "partition_bounds": partition_bounds,
            "hn_client": hn_api_subsample_client.configured({"sample_rate": 10}),
        },
        **RESOURCES_STAGING,
    },
    tags=DOWNLOAD_TAGS,
    config=hourly_download_config,
)

download_local_job = hacker_news_api_download.to_job(
    resource_defs={
        **{"partition_bounds": partition_bounds, "hn_client": hn_snapshot_client},
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