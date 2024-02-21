import logging

from okdata.sdk.data.dataset import Dataset
from okdata.sdk.data.upload import Upload
from requests.exceptions import HTTPError

logger = logging.getLogger()


def upload_dataset(dataset_id, filename):
    logger.info(f"Uploading dataset, id={dataset_id}, file={filename}")

    dataset = Dataset()
    upload = Upload()

    try:
        version = dataset.get_latest_version(dataset_id)["version"]
    except HTTPError as e:
        if e.response.status_code == 404:
            print(f"Dataset '{dataset_id}' not found; skipping import")
            return
        raise

    edition = dataset.auto_create_edition(dataset_id, version)["Id"].split("/")[-1]
    upload.upload(filename, dataset_id, version, edition, 3)
