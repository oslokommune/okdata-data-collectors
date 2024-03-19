import asyncio
import logging
from pathlib import Path

from aiohttp import ClientSession, ClientResponseError
from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws import ssm
from okdata.aws.logging import logging_wrapper

from common import dataplatform, util

patch_all()
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

MEASUREMENTS = {
    "fdeYObXg1OpTh1XxXPJ4": "dataspeilet-antall-malinger-i-origo",
    "iRznHuvBqx2ketpA8keT": "dataspeilet-etterlevelse-av-oppdateringshyppighet",
}


async def collect_measurements(measurements):
    # Fetch values for all measurements
    logger.info(f"Fetching data for {len(measurements)} measurements")
    api_key = ssm.get_secret("/dataplatform/okr-tracker/api-key")

    async with ClientSession(
        headers={"x-api-key": api_key},
        base_url=util.getenv("OKR_TRACKER_API_BASE_URL"),
        raise_for_status=True,
    ) as session:
        kpis = await asyncio.gather(
            *[fetch_measurement(session, kpi_id) for kpi_id in measurements.keys()]
        )

    measurements_data = {measurement_id: values for measurement_id, values in kpis}

    # Upload data to dataset
    for measurement_id, dataset_id in measurements.items():
        measurement_values = measurements_data[measurement_id]

        if measurement_values is None:
            logger.warning(
                f"No data for measurement '{measurement_id}'; skipping import!"
            )
            continue

        logger.info(
            f"Uploading {len(measurement_values)} measurement values for to dataset '{dataset_id}'"
        )

        csv_file = util.write_dict_to_csv(
            filename=Path("/") / "tmp" / f"{dataset_id}_values.csv",
            data=measurement_values,
            fieldnames=["date", "value", "comment"],
            extrasaction="ignore",
        )

        dataplatform.upload_dataset(dataset_id, csv_file.name)


async def fetch_measurement(session, measurement_id):
    try:
        async with session.get(f"/kpi/{measurement_id}/values") as response:
            response_data = await response.json()
            return (
                measurement_id,
                [
                    {
                        "date": v["date"],
                        "value": v["value"],
                        "comment": (v["comment"] or "").replace("\n", " "),
                    }
                    for v in response_data
                ],
            )
    except ClientResponseError as e:
        logger.error(
            "Error while fetching measurement `{}`: {}".format(
                measurement_id,
                str(e),
            )
        )
    return (measurement_id, None)


@logging_wrapper
@xray_recorder.capture("collect_monitors")
def import_data(event, context):
    asyncio.run(collect_measurements(MEASUREMENTS))
