import logging
import re
from functools import cache

from okdata.aws import ssm
from okdata.sdk.config import Config
from okdata.sdk.data.dataset import Dataset
from okdata.sdk.data.upload import Upload
from okdata.sdk.pipelines.client import PipelineApiClient
from requests.exceptions import HTTPError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@cache
def _sdk_config():
    sdk_config = Config()
    sdk_config.config["client_secret"] = ssm.get_secret(
        "/dataplatform/okdata-data-collectors/keycloak-client-secret"
    )
    return sdk_config


class Dataplatform:
    def __init__(self):
        self.sdk_config = _sdk_config()
        self.dataset_client = Dataset(self.sdk_config)
        self.pipeline_client = PipelineApiClient(self.sdk_config)
        self.upload_client = Upload(self.sdk_config)

    def get_datasets(self, parent_id=None, was_derived_from_name=None):
        metadata_api_url = self.sdk_config.get("datasetUrl")
        result = self.dataset_client.get(
            url=metadata_api_url,
            params={
                "parent_id": parent_id,
                "was_derived_from_name": was_derived_from_name,
            },
        )
        return result.json()

    def create_dataset(self, metadata, pipeline=None):
        metadata = _clean_dataset_metadata(metadata)

        logger.info(f"Creating dataset with title '{metadata['title']}'")

        dataset = self.dataset_client.create_dataset(data=metadata)

        if pipeline:
            self.create_pipeline(dataset["Id"], pipeline)

        return dataset

    def create_pipeline(self, dataset_id, pipeline_processor_id):
        logger.info(
            f"Creating {pipeline_processor_id} pipeline for dataset '{dataset_id}'"
        )

        pipeline_id = self.pipeline_client.create_pipeline_instance(
            {
                "pipelineProcessorId": pipeline_processor_id,
                "id": dataset_id,
                "datasetUri": f"output/{dataset_id}/1",
            }
        ).strip('"')

        pipeline_input_id = self.pipeline_client.create_pipeline_input(
            {
                "pipelineInstanceId": pipeline_id,
                "datasetUri": f"input/{dataset_id}/1",
                "stage": "raw",
            }
        ).strip('"')

        logger.info(f"Created pipeline, id={pipeline_id}, input_id={pipeline_input_id}")

    def upload_dataset(self, dataset_id, filename):
        logger.info(f"Uploading dataset, id={dataset_id}, file={filename}")

        try:
            version = self.dataset_client.get_latest_version(dataset_id)["version"]
        except HTTPError as e:
            if e.response.status_code == 404:
                logger.error(f"Dataset '{dataset_id}' not found; skipping import")
                return None
            raise

        edition = self.dataset_client.auto_create_edition(dataset_id, version)[
            "Id"
        ].split("/")[-1]

        return self.upload_client.upload(filename, dataset_id, version, edition, 3)


def upload_dataset(dataset_id, filename):
    return Dataplatform().upload_dataset(dataset_id, filename)


def _clean_dataset_metadata(metadata):
    metadata["title"] = re.sub(
        r"[^- a-zA-Z0-9åÅæÆøØ]",
        "",
        metadata["title"],
    )[0:128]

    if "description" in metadata:
        metadata["description"] = metadata["description"][0:2048]

    return metadata
