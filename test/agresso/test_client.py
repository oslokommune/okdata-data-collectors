from freezegun import freeze_time

from agresso.client import _current_and_past_periods, _all_periods


@freeze_time("2024-05-01T12:00:00+00:00")
def test_current_and_past_periods_current():
    assert _current_and_past_periods(2024) == [
        "202401",
        "202402",
        "202403",
        "202404",
        "202405",
    ]


@freeze_time("2024-05-01T12:00:00+00:00")
def test_current_and_past_periods_past():
    assert _current_and_past_periods(2023) == [
        "202301",
        "202302",
        "202303",
        "202304",
        "202305",
        "202306",
        "202307",
        "202308",
        "202309",
        "202310",
        "202311",
        "202312",
    ]


@freeze_time("2024-05-01T12:00:00+00:00")
def test_current_and_past_periods_future():
    assert _current_and_past_periods(2025) == []


def test_all_periods():
    assert _all_periods(2024) == [
        "202401",
        "202402",
        "202403",
        "202404",
        "202405",
        "202406",
        "202407",
        "202408",
        "202409",
        "202410",
        "202411",
        "202412",
    ]
