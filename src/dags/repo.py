from dagster import build_schedule_from_partitioned_job, repository
from dags.jobs.scrape_onyx import (
    scrape_onyx_prod,
    scrape_onyx_test
)


@repository
def onyx_prod():
    return [scrape_onyx_prod]

@repository
def onyx_test():
    return [scrape_onyx_test]
