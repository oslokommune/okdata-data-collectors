import logging
from functools import cache

from okdata.aws.ssm import get_secret
from okdata.sdk.config import Config
from okdata.sdk.data.dataset import Dataset
from okdata.sdk.data.upload import Upload
from requests.exceptions import HTTPError

logger = logging.getLogger()


@cache
def _sdk_config():
    sdk_config = Config()
    sdk_config.config["client_secret"] = get_secret(
        "/dataplatform/okdata-data-collectors/keycloak-client-secret"
    )
    return sdk_config


def upload_dataset(dataset_id, filename):
    logger.info(f"Uploading dataset, id={dataset_id}, file={filename}")

    sdk_config = _sdk_config()
    dataset = Dataset(sdk_config)
    upload = Upload(sdk_config)

    try:
        version = dataset.get_latest_version(dataset_id)["version"]
    except HTTPError as e:
        if e.response.status_code == 404:
            logger.error(f"Dataset '{dataset_id}' not found; skipping import")
            return
        raise

    edition = dataset.auto_create_edition(dataset_id, version)["Id"].split("/")[-1]
    upload.upload(filename, dataset_id, version, edition, 3)
