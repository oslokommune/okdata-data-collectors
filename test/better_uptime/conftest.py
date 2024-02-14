import re

import pytest
from unittest.mock import patch

from common import ssm


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
        # /monitors[?page={page_num}]
        if match := re.search(
            r"\/api\/v2\/monitors(\?page\=(?P<page_num>[0-9]+))?$", url
        ):
            page_num = int(match.group("page_num")) if match.group("page_num") else 1
            return AsyncMock(200, response_data["monitors"][(page_num - 1)])

        # /monitors/{id}/sla
        if match := re.search(
            r"\/api\/v2\/monitors\/(?P<monitor_id>[0-9]+)\/sla$", url
        ):
            return AsyncMock(
                200, {"data": response_data["sla"][match.group("monitor_id")]}
            )

        # /monitor-groups[?page={page_num}]
        if match := re.search(
            r"\/api\/v2\/monitor\-groups(\?page\=(?P<page_num>[0-9]+))?$", url
        ):
            page_num = int(match.group("page_num")) if match.group("page_num") else 1
            return AsyncMock(200, response_data["groups"][(page_num - 1)])

    monkeypatch.setattr("aiohttp.ClientSession.get", mock_client_get)
