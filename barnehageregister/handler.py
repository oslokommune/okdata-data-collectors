import json
import logging
import tempfile

from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws.logging import logging_wrapper

from common.dataplatform import upload_dataset
from barnehageregister.service import kindergartens_in_oslo

patch_all()

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def upload_data(dataset_id, data):
    if not data:
        logger.info(f"Skipping empty dataset {dataset_id}")
        return

    logger.info(f"Uploading data to dataset '{dataset_id}'")

    with tempfile.NamedTemporaryFile("w", suffix=".json") as f:
        f.write(json.dumps(data))
        f.seek(0)
        res = upload_dataset(dataset_id, f.name)

    logger.info(f"Upload done, code={res['result']}, trace_id={res['trace_id']}")


@logging_wrapper
@xray_recorder.capture("import_datasets")
def import_datasets(event, context):
    upload_data("nbr-barnehager-i-oslo", kindergartens_in_oslo())
