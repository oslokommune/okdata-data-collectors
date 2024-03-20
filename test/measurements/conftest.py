import re

import pytest
from unittest.mock import patch

from okdata.aws import ssm


@pytest.fixture(autouse=True)
def mocked_ssm_get_secret():
    with patch.object(ssm, "get_secret", return_value="foo-token"):
        yield


class AsyncMock:
    def __init__(self, status_code, data):
        self.status = status_code
        self._response_data = data

    async def __aenter__(self):
        return self

    async def __aexit__(self, *error_info):
        return self

    async def json(self):
        return self._response_data


@pytest.fixture(scope="function")
def mock_client(monkeypatch, response_data):
    def mock_client_get(self, url):
        # /kpi/{measurement_id}/values
        if match := re.search(r"\/kpi\/(?P<measurement_id>[a-zA-Z0-9]+)\/values$", url):
            measurement_values = response_data.get(match.group("measurement_id"))
            if measurement_values is not None:
                return AsyncMock(200, measurement_values)
        return AsyncMock(404, None)

    monkeypatch.setattr("aiohttp.ClientSession.get", mock_client_get)
