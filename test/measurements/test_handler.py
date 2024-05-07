import csv
from pathlib import Path

import pytest
from aws_xray_sdk.core import xray_recorder
from unittest.mock import ANY, call

import measurements.handler as handler
from common.dataplatform import Dataplatform
from test.measurements import mockdata

xray_recorder.begin_segment("Test")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "measurements,kpi_responses,get_datasets_response,create_dataset_responses",
    [
        mockdata.create_test_case(
            ["bF546", "BxN5k", "Ac3Dk", "6FW0s", "a4b04"],
            [
                {
                    "kpi_id": "bF546",
                    "name": "Magic blasts fired",
                    "description": "Number of magic blasts fired",
                    "parent": "Team Magikoopas",
                    "value_count": 3,
                    "dataset_exists": True,
                },
                {
                    "kpi_id": "BxN5k",
                    "name": "Magic blast hits",
                    "description": "Number of magic blast hits",
                    "parent": "Team Magikoopas",
                    "value_count": 2,
                    "dataset_exists": False,
                },
                {
                    "kpi_id": "Ac3Dk",
                    "name": "Baby Luigi kidnaps",
                    "description": "Number Baby Luigi kidnaps",
                    "parent": None,
                    "value_count": 1,
                    "dataset_exists": False,
                },
                {
                    "kpi_id": "6FW0s",
                    "name": "Pyrokinesis success rate",
                    "description": "Main result indicator",
                    "parent": "Team Magikoopas",
                    "value_count": 0,
                    "dataset_exists": False,
                },
            ],
        ),
    ],
)
async def test_collect_measurements(
    mocked_client,
    mocked_dataplatform,
    measurements,
    kpi_responses,
    get_datasets_response,
    create_dataset_responses,
    mocker,
):
    get_datasets_spy = mocker.spy(Dataplatform, "get_datasets")
    create_dataset_spy = mocker.spy(Dataplatform, "create_dataset")
    create_pipeline_spy = mocker.spy(Dataplatform, "create_pipeline")
    upload_dataset_spy = mocker.spy(Dataplatform, "upload_dataset")

    await handler.collect_measurements(measurements)

    get_datasets_spy.assert_called_once_with(
        ANY,
        was_derived_from_name="okr-tracker",
    )

    existing_mapping = {
        ds["wasDerivedFrom"]["id"]: ds["Id"] for ds in get_datasets_response
    }
    created_mapping = {
        ds["wasDerivedFrom"]["id"]: ds["Id"] for ds in create_dataset_responses
    }

    assert create_dataset_spy.call_count == len(created_mapping)
    for create_call in create_dataset_spy.call_args_list:
        dataset_metadata = create_call[1]["metadata"]
        source_kpi_id = dataset_metadata["wasDerivedFrom"]["id"]

        assert source_kpi_id not in existing_mapping
        assert source_kpi_id in created_mapping

        assert len(dataset_metadata["title"]) <= 128
        assert len(dataset_metadata["description"]) <= 2048

    assert create_pipeline_spy.call_count == len(created_mapping)
    create_pipeline_spy.assert_has_calls(
        [
            call(ANY, dataset_id, "csv-to-delta")
            for dataset_id in created_mapping.values()
        ]
    )

    for kpi_id, dataset_id in {**existing_mapping, **created_mapping}.items():
        csv_file_path = Path("/") / "tmp" / f"{dataset_id}_values.csv"
        response_values = kpi_responses[kpi_id][1]

        with open(csv_file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            records = list(reader)

            assert reader.dialect == "excel"
            assert reader.fieldnames == ["date", "value", "comment"]

            assert len(records) == len(response_values)

            for i, record in enumerate(records):
                assert record == {
                    field: (
                        str(response_values[i][field])
                        if response_values[i][field] is not None
                        else ""
                    )
                    for field in reader.fieldnames
                }

            upload_dataset_spy.assert_any_call(ANY, dataset_id, str(csv_file_path))

    assert upload_dataset_spy.call_count == len(kpi_responses)
