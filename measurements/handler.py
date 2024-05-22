import asyncio
import logging
from pathlib import Path

from aiohttp import ClientSession, ClientResponseError
from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws import ssm
from okdata.aws.logging import logging_wrapper

from common import util
from common.dataplatform import Dataplatform
from measurements.config import MEASUREMENTS

patch_all()
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


async def collect_measurements(measurements):
    dataplatform = Dataplatform()

    # Get existing datasets with the OKR tracker as source
    logger.info("Fetching existing measurement datasets")
    kpi_datasets = dataplatform.get_datasets(
        was_derived_from_name="okr-tracker",
    )
    logger.info(f"Found {len(kpi_datasets)} existing dataset(s)")

    # Fetch values for all measurements
    logger.info(f"Fetching data for {len(measurements)} measurement(s)")
    api_key = ssm.get_secret("/dataplatform/okr-tracker/api-key")

    async with ClientSession(
        headers={"x-api-key": api_key},
        base_url=util.getenv("OKR_TRACKER_API_BASE_URL"),
        raise_for_status=True,
    ) as session:
        kpis = await asyncio.gather(
            *[fetch_measurement(session, kpi_id) for kpi_id in measurements]
        )

    for kpi_id, kpi, kpi_values in kpis:
        if kpi is None or kpi_values is None:
            logger.warning(f"No data for measurement '{kpi_id}'; skipping import!")
            continue

        kpi_id = kpi["id"]
        matched_datasets = [
            d for d in kpi_datasets if d.get("wasDerivedFrom", {}).get("id") == kpi_id
        ]

        if not matched_datasets and util.getenv("STAGE") == "dev":
            # Skip import of additional datasets in dev.
            logger.info(
                f"Skipped creating missing dataset for measurement '{kpi_id}' in dev"
            )
            continue

        dataset = (
            matched_datasets[0]
            if matched_datasets
            else create_kpi_dataset(dataplatform, kpi)
        )
        dataset_id = dataset["Id"]

        logger.info(
            f"Uploading {len(kpi_values)} measurement value(s) to dataset '{dataset_id}'"
        )

        csv_file = util.write_dict_to_csv(
            filename=Path("/") / "tmp" / f"{dataset_id}_values.csv",
            data=kpi_values,
            fieldnames=["date", "value", "comment"],
            extrasaction="ignore",
        )

        result = dataplatform.upload_dataset(dataset_id, csv_file.name)
        logger.info(
            f"Upload done, code={result['result']}, trace_id={result['trace_id']}"
        )


async def fetch_measurement(session, kpi_id):
    try:
        async with session.get(f"/kpi/{kpi_id}") as response:
            data = await response.json()

        kpi = {
            "id": data["id"],
            "name": data["name"],
            "description": data["description"],
            "parent_slug": data["parent"]["slug"] if data["parent"] else None,
            "parent_name": data["parent"]["name"] if data["parent"] else None,
        }

        async with session.get(f"/kpi/{kpi_id}/values") as response:
            data = await response.json()

        kpi_values = [
            {
                "date": v["date"],
                "value": v["value"],
                "comment": (v["comment"] or "").replace("\n", " "),
            }
            for v in data
        ]

        return (kpi_id, kpi, kpi_values)

    except ClientResponseError as e:
        logger.error(
            "Error while fetching measurement `{}`: {}".format(
                kpi_id,
                str(e),
            )
        )
    return (kpi_id, None, None)


def create_kpi_dataset(dataplatform, kpi):
    logger.info(f"Creating missing dataset for measurement '{kpi['id']}'")

    dataset_title = (
        f"{kpi['parent_name']} - {kpi['name']}" if kpi["parent_name"] else kpi["name"]
    )
    dataset_description = kpi["description"] if kpi["description"] else ""
    dataset_keywords = ["måling"]
    if parent_slug := kpi["parent_slug"]:
        dataset_keywords.append(parent_slug)

    return dataplatform.create_dataset(
        metadata={
            "title": dataset_title,
            "description": dataset_description,
            "keywords": dataset_keywords,
            "accessRights": "restricted",
            "source": {"type": "file"},
            "wasDerivedFrom": {"name": "okr-tracker", "id": kpi["id"]},
            "contactPoint": {
                "name": "Dataspeilet",
                "email": "dataspeilet@oslo.kommune.no",
            },
            "publisher": "Oslo Origo",
        },
        pipeline="csv-to-delta",
    )


@logging_wrapper
@xray_recorder.capture("collect_monitors")
def import_data(event, context):
    asyncio.run(collect_measurements(MEASUREMENTS))
