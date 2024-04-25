from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws.logging import logging_wrapper

from common.dataplatform import upload_dataset
from ssb.client import get_dataset

patch_all()

# Mapping of SSB dataset by ID to Origo Dataplatform dataset by ID.
# Available SSB datasets are listed at: https://data.ssb.no/api/v0/dataset/.
DATASETS = {
    "26975": "ssb-befolkning-per-kommune",
}


def _import_dataset(dataset_id, data):
    with open(f"/tmp/{dataset_id}.csv", "w") as tmpfile:
        tmpfile.write(data)
        tmpfile.seek(0)
        upload_dataset(dataset_id, tmpfile.name)


@logging_wrapper
@xray_recorder.capture("import_datasets")
def import_datasets(event, context):
    for ssb_dataset_id, dataset_id in DATASETS.items():
        _import_dataset(dataset_id, get_dataset(ssb_dataset_id))
