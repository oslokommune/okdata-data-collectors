from unittest.mock import ANY, Mock, patch

from statistikkbanken.handler import create_dataset, import_datasets, upload_data


def test_create_dataset():
    dataplatform_mock = Mock()
    create_dataset("Foo", "da0de9b3-6f2f-2c93-fb8f-a3b2422ebb67", dataplatform_mock)
    dataplatform_mock.create_dataset.assert_called_once()


def test_upload_data():
    dataplatform_mock = Mock()
    dataplatform_mock.upload_dataset.return_value = {"result": "ok", "trace_id": 123}

    upload_data("foo", "a\tb\tc\n1\t2\t3", dataplatform_mock)

    dataplatform_mock.upload_dataset.assert_called_once_with("foo", ANY)


@patch(
    "statistikkbanken.handler.DATASETS",
    [
        {"table_id": "ABC123", "title": "Foo", "query_id": "foo"},
        {"table_id": "DEF456", "title": "Bar", "query_id": "bar"},
    ],
)
@patch("statistikkbanken.handler.upload_data")
@patch("statistikkbanken.handler.create_dataset")
@patch("statistikkbanken.handler.query_statistikkbanken")
@patch("statistikkbanken.handler.Dataplatform")
def test_import_datasets_existing(
    mock_dataplatform,
    mock_query_statistikkbanken,
    mock_create_dataset,
    mock_upload_data,
):
    mock_dataplatform.return_value.get_datasets.return_value = [
        {
            "Id": "bar",
            "wasDerivedFrom": {"id": "bar"},
        }
    ]

    import_datasets({}, None)

    assert mock_create_dataset.call_count == 1
    assert mock_upload_data.call_count == 2
