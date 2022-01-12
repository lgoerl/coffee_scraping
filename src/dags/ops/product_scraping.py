from pandas import DataFrame
from typing import List

from dagster import op, DynamicOut
from dags.resources.api_client.base_api_scraper import return_columns

@op(
    required_resource_keys={"api_client"},
    out=DynamicOut(str),
    )
def get_product_list(context):
    products = context.resources.api_client.get_active_roasts()
    for product in products:
        yield DynamicOut(
            value=product,
            mapping_key=product.replace("/", "_"),
        )

@op(required_resource_keys={"api_client"})
def get_product_info(context, product: str):
    return context.resources.api_client.get_roast(product)

@op()
def process_product_collection(products: List[dict]) -> DataFrame:
    return DataFrame.from_records(products)[return_columns]
