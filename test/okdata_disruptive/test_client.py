"""Integration tests for the Disruptive API client.

Set `DISRUPTIVE_PROJECT_ID`, `DISRUPTIVE_SERVICE_ACCOUNT_EMAIL`, `DISRUPTIVE_SERVICE_ACCOUNT_KEY_ID`,
and `DISRUPTIVE_SERVICE_ACCOUNT_SECRET` temporarily in `tox.ini` to run these tests
against the real Disruptive API, which is mostly useful during development.
"""

import os

import pytest

from okdata_disruptive.client import DisruptiveClient


def _is_configured():
    return (
        "DISRUPTIVE_PROJECT_ID" in os.environ
        and "DISRUPTIVE_SERVICE_ACCOUNT_EMAIL" in os.environ
        and "DISRUPTIVE_SERVICE_ACCOUNT_KEY_ID" in os.environ
        and "DISRUPTIVE_SERVICE_ACCOUNT_SECRET" in os.environ
    )


@pytest.mark.skipif(not _is_configured(), reason="not configured")
def test_get_project():
    disruptive_client = DisruptiveClient(
        os.environ["DISRUPTIVE_SERVICE_ACCOUNT_EMAIL"],
        os.environ["DISRUPTIVE_SERVICE_ACCOUNT_KEY_ID"],
        os.environ["DISRUPTIVE_SERVICE_ACCOUNT_SECRET"],
    )
    project = disruptive_client.get_project(os.environ["DISRUPTIVE_PROJECT_ID"])
    assert project.project_id == os.environ["DISRUPTIVE_PROJECT_ID"]


@pytest.mark.skipif(not _is_configured(), reason="not configured")
def test_list_devices():
    disruptive_client = DisruptiveClient(
        os.environ["DISRUPTIVE_SERVICE_ACCOUNT_EMAIL"],
        os.environ["DISRUPTIVE_SERVICE_ACCOUNT_KEY_ID"],
        os.environ["DISRUPTIVE_SERVICE_ACCOUNT_SECRET"],
    )
    devices = disruptive_client.list_devices(os.environ["DISRUPTIVE_PROJECT_ID"])
    assert len(devices) > 0


@pytest.mark.skipif(not _is_configured(), reason="not configured")
def test_get_events():
    disruptive_client = DisruptiveClient(
        os.environ["DISRUPTIVE_SERVICE_ACCOUNT_EMAIL"],
        os.environ["DISRUPTIVE_SERVICE_ACCOUNT_KEY_ID"],
        os.environ["DISRUPTIVE_SERVICE_ACCOUNT_SECRET"],
    )
    project = disruptive_client.get_project(os.environ["DISRUPTIVE_PROJECT_ID"])
    devices = disruptive_client.list_devices(os.environ["DISRUPTIVE_PROJECT_ID"])
    events = disruptive_client.get_events(project, devices[0])
    assert len(events) > 0
