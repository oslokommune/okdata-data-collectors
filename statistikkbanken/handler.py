import logging
import tempfile

from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws.logging import logging_wrapper

from common.dataplatform import Dataplatform
from statistikkbanken.client import query_statistikkbanken
from statistikkbanken.config import DATASETS

patch_all()
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_dataset(title, query_id, dataplatform):
    logger.info(f"Creating missing dataset for dataset with title '{title}'")

    return dataplatform.create_dataset(
        metadata={
            "title": title,
            "description": f"{title} (Statistikkbanken)",
            "keywords": ["statistikkbanken"],
            "accessRights": "public",
            "source": {"type": "file"},
            "wasDerivedFrom": {"name": "statistikkbanken", "id": query_id},
            "contactPoint": {
                "name": "Dataspeilet",
                "email": "dataspeilet@oslo.kommune.no",
            },
            "publisher": "Byrådsavdeling for finans",
        },
        pipeline="csv-to-delta",
    )


def upload_data(dataset_id, data, dataplatform):
    logger.info(f"Uploading data to dataset '{dataset_id}'")

    with tempfile.NamedTemporaryFile("w", suffix=".csv") as f:
        f.write(data)
        f.seek(0)
        res = dataplatform.upload_dataset(dataset_id, f.name)

    logger.info(f"Upload done, code={res['result']}, trace_id={res['trace_id']}")


@logging_wrapper
@xray_recorder.capture("import_datasets")
def import_datasets(event, context):
    dataplatform = Dataplatform()
    existing_datasets = dataplatform.get_datasets(
        was_derived_from_name="statistikkbanken"
    )
    logger.info(
        "Found {} existing dataset{}".format(
            len(existing_datasets),
            "s" if len(existing_datasets) > 1 else "",
        )
    )

    for ds in DATASETS:
        title, query_id = ds["title"], ds["query_id"]
        matched_datasets = [
            ds
            for ds in existing_datasets
            if ds.get("wasDerivedFrom", {}).get("id") == query_id
        ]
        dataset = (
            matched_datasets[0]
            if matched_datasets
            else create_dataset(title, query_id, dataplatform)
        )

        data = query_statistikkbanken(query_id)
        upload_data(dataset["Id"], data, dataplatform)
