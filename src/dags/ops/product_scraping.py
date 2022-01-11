from dagster import op

@op(required_resource_keys={"api_client"})
def get_product_list(context):
    return context.resources.api_client.get_active_roasts()

@op(required_resource_keys={"api_client"})
def get_product_info(context, product):
    return context.resources.api_client.get_roast(product)