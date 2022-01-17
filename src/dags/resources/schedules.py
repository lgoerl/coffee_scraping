from datetime import datetime
from dagster import daily_partitioned_config

@daily_partitioned_config(start_date=datetime(2022, 1, 15))
def daily_partitioned_config(start: datetime, end: datetime):
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