import asyncio
import csv
import logging

from aiohttp import ClientSession
from aws_xray_sdk.core import patch_all, xray_recorder

from okdata.aws.logging import logging_wrapper

from better_uptime.client import BetterUptimeClient

from common import dataplatform, ssm, util

patch_all()
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

DATASET_ID = util.getenv("UPTIME_DATASET_ID")
OUTPUT_CSV_TEMP_PATH = "/tmp/uptime_data.csv"
OUTPUT_CSV_FIELD_NAMES = [
    "id",
    "monitor_type",
    "name",
    "group_name",
    "created_at",
    "updated_at",
    "paused",
    "last_checked_at",
    "availability",
    "total_downtime",
    "number_of_incidents",
    "longest_incident",
    "average_incident",
]


async def fetch_all_monitors():
    logger.info("Fetching monitors from Better Uptime")
    access_token = ssm.get_secret("/dataplatform/betteruptime/api-token")
    bu_client = BetterUptimeClient()

    async with ClientSession(
        raise_for_status=True,
        headers={"Authorization": f"Bearer {access_token}"},
    ) as session:
        monitors, monitor_groups = await asyncio.gather(
            *[bu_client.monitors(session), bu_client.monitor_groups(session)]
        )
        monitor_slas = await asyncio.gather(
            *[bu_client.sla(session, monitor_id=monitor["id"]) for monitor in monitors]
        )

    logger.info(
        "Got data, monitors={}, groups={}, SLAs={}".format(
            len(monitors),
            len(monitor_groups),
            len(monitor_slas),
        )
    )

    groups = {g["id"]: g["attributes"] for g in monitor_groups}
    slas = {m["id"]: m["attributes"] for m in monitor_slas}
    monitor_data = []

    for monitor in monitors:
        attrs = monitor["attributes"]
        group_id = attrs.get("monitor_group_id")
        group_name = groups.get(str(group_id), {}).get("name") if group_id else None
        sla = slas.get(str(monitor["id"]))

        monitor_data.append(
            {
                "id": monitor["id"],
                "name": attrs["pronounceable_name"],
                "group_name": group_name,
                "monitor_type": attrs["monitor_type"],
                "created_at": attrs["created_at"],
                "updated_at": attrs["updated_at"],
                "paused": str(attrs["paused"]).lower(),
                "last_checked_at": attrs["last_checked_at"],
                **sla,
            }
        )

    return monitor_data


async def import_dataset():
    monitors = await fetch_all_monitors()

    with open(OUTPUT_CSV_TEMP_PATH, "w") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            extrasaction="ignore",
            fieldnames=OUTPUT_CSV_FIELD_NAMES,
        )

        writer.writeheader()

        logger.info(f"Writing {len(monitors)} rows to CSV")

        for monitor in monitors:
            writer.writerow(monitor)

    logger.info(f"Uploading data to dataset {DATASET_ID}")
    dataplatform.upload_dataset(DATASET_ID, csvfile.name)


@logging_wrapper
@xray_recorder.capture("collect_monitors")
def collect_monitors(event, context):
    asyncio.run(import_dataset())


if __name__ == "__main__":
    collect_monitors(None, None)
