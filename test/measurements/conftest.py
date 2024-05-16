import re
from unittest.mock import patch

import pytest
from aiohttp import ClientResponseError, RequestInfo
from okdata.aws import ssm
from okdata.sdk.data.dataset import Dataset
from okdata.sdk.data.upload import Upload
from okdata.sdk.pipelines.client import PipelineApiClient


@pytest.fixture(autouse=True)
def mocked_ssm_get_secret():
    with patch.object(ssm, "get_secret", return_value="foo-token"):
        yield


class AsyncMock:
    def __init__(self, status_code, url, data):
        self.status = status_code
        self._response_data = data

        if self.status >= 400:
            info = RequestInfo(url=url, method="GET", headers={})
            raise ClientResponseError(request_info=info, status=self.status, history=[])

    async def __aenter__(self):
        return self

    async def __aexit__(self, *error_info):
        return self

    async def json(self):
        return self._response_data


@pytest.fixture(scope="function")
def mocked_client(monkeypatch, kpi_responses):
    def mock_client_get(self, url):
        # /kpi/{measurement_id}
        if match := re.search(r"\/kpi\/(?P<measurement_id>[a-zA-Z0-9]+)$", url):
            if response := kpi_responses.get(match.group("measurement_id")):
                return AsyncMock(200, url, response[0])

        # /kpi/{measurement_id}/values
        if match := re.search(r"\/kpi\/(?P<measurement_id>[a-zA-Z0-9]+)\/values$", url):
            if response := kpi_responses.get(match.group("measurement_id")):
                return AsyncMock(200, url, response[1])

        return AsyncMock(404, url, None)

    monkeypatch.setattr("aiohttp.ClientSession.get", mock_client_get)


@pytest.fixture()
def mocked_dataplatform(
    monkeypatch,
    get_datasets_response,
    create_dataset_responses,
):
    def custom_get(self, url, **kwargs):
        class MockResponse:
            def json(self):
                return get_datasets_response

        return MockResponse()

    def get_latest_version(self, dataset_id):
        return {"version": 1}

    def create_dataset(self, data):
        for dataset in create_dataset_responses:
            if dataset["wasDerivedFrom"]["id"] == data["wasDerivedFrom"]["id"]:
                return dataset

    def auto_create_edition(self, dataset_id, version):
        return {"Id": f"{dataset_id}/{version}/20240101T102336"}

    def upload(self, file_name, dataset_id, version_id, edition_id, retries):
        return {"result": True, "trace_id": "foo-trace-id"}

    def create_pipeline_instance(self, data):
        return "pipeline-instance-id"

    def create_pipeline_input(self, data):
        return "pipeline-input-id"

    monkeypatch.setattr(Dataset, "get", custom_get)
    monkeypatch.setattr(Dataset, "get_latest_version", get_latest_version)
    monkeypatch.setattr(Dataset, "create_dataset", create_dataset)
    monkeypatch.setattr(Dataset, "auto_create_edition", auto_create_edition)
    monkeypatch.setattr(Upload, "upload", upload)
    monkeypatch.setattr(
        PipelineApiClient, "create_pipeline_instance", create_pipeline_instance
    )
    monkeypatch.setattr(
        PipelineApiClient, "create_pipeline_input", create_pipeline_input
    )
