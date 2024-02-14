import csv
from unittest.mock import patch

import pytest
from aws_xray_sdk.core import xray_recorder

import better_uptime.handler as handler
from better_uptime.client import BU_MAX_PAGES, IterationLimitExceededError
from common import dataplatform
from test.better_uptime import util

xray_recorder.begin_segment("Test")


default_mock_data = {
    "groups": [
        util.create_group(1, "Public"),
        util.create_group(2, "Internal"),
        util.create_group(3, "Services"),
    ],
    "monitors": [
        util.create_monitor(1, "foo_foo", "foo.com/foo", group_id=1),
        util.create_monitor(2, "foo_bar", "foo.com/bar", group_id=1),
        util.create_monitor(3, "bar", "bar.com", group_id=2),
        util.create_monitor(4, "baz", "baz.com"),
        util.create_monitor(5, "ham", "ham.com", paused=True),
    ],
    "per_page": 2,
}


def test_collect_monitors(mocker):
    import_dataset_mock = mocker.patch.object(handler, "import_dataset")
    handler.collect_monitors({}, {})
    import_dataset_mock.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data",
    [util.create_response_data(**default_mock_data)],
)
async def test_fetch_all_monitors(mock_client):
    monitors = await handler.fetch_all_monitors()
    assert len(monitors) == 5
    assert len([m for m in monitors if m["group_name"] == "Public"]) == 2
    assert len([m for m in monitors if m["group_name"] == "Internal"]) == 1
    assert len([m for m in monitors if m["group_name"] == "Services"]) == 0
    assert len([m for m in monitors if m["group_name"] is None]) == 2
    assert len([m for m in monitors if m["paused"] == "true"]) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data",
    [
        util.create_response_data(
            monitors=[
                util.create_monitor(i, "foo", "foo.com")
                for i in range(1, BU_MAX_PAGES + 1)
            ],
            per_page=1,
        )
    ],
)
async def test_fetch_all_monitors_no_infinite_loop(mock_client):
    with pytest.raises(IterationLimitExceededError):
        await handler.fetch_all_monitors()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data",
    [util.create_response_data(**default_mock_data)],
)
@patch.object(dataplatform, "upload_dataset")
async def test_import_dataset(mock_dataset_upload, mock_client, response_data):
    await handler.import_dataset()

    with open(handler.OUTPUT_CSV_TEMP_PATH, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        records = list(reader)

        assert reader.dialect == "excel"
        assert reader.fieldnames == handler.OUTPUT_CSV_FIELD_NAMES
        assert len(records) == sum([len(p["data"]) for p in response_data["monitors"]])

        assert records[0]["id"] == "1"
        assert records[0]["name"] == "foo_foo"
        assert records[0]["group_name"] == "Public"
        assert records[0]["availability"] == "100.0"

        mock_dataset_upload.assert_called_once_with(
            handler.DATASET_ID, handler.OUTPUT_CSV_TEMP_PATH
        )
