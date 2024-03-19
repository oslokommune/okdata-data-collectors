import csv
from pathlib import Path

import pytest
from aws_xray_sdk.core import xray_recorder
from unittest.mock import patch

import measurements.handler as handler
from common import dataplatform

xray_recorder.begin_segment("Test")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "response_data",
    [
        {
            "foo456": [
                {
                    "value": 0.14,
                    "date": "2024-02-18",
                    "comment": "foooo",
                    "created": "2024-02-18T20:03:12.871Z",
                },
                {
                    "value": 0.7,
                    "date": "2024-01-10",
                    "comment": None,
                    "created": "2024-01-10T20:03:12.871Z",
                },
            ],
            "bar456": [],
        }
    ],
)
@patch.object(dataplatform, "upload_dataset")
async def test_collect_measurements(
    mock_dataset_upload,
    mock_client,
    response_data,
    mocker,
):
    measurements = {
        "foo456": "foo-dataset",
        "bar456": "bar-dataset",
        "baz789": "baz-dataset",
    }

    await handler.collect_measurements(measurements)

    for measurement_id, dataset_id in measurements.items():
        csv_file_path = Path("/") / "tmp" / f"{dataset_id}_values.csv"

        response_values = response_data.get(measurement_id)

        if response_values is None:
            assert not csv_file_path.exists()
            continue

        with open(csv_file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            records = list(reader)

            assert reader.dialect == "excel"
            assert reader.fieldnames == ["date", "value", "comment"]

            assert len(records) == len(response_values)

            for i, record in enumerate(records):
                assert record == {
                    field: str(response_values[i][field] or "")
                    for field in reader.fieldnames
                }

        assert (
            mocker.call(dataset_id, str(csv_file_path))
            in mock_dataset_upload.call_args_list
        )

    assert mock_dataset_upload.call_count == len(response_data)
