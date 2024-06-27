"""Integration tests for the Agresso API service.

Set `AGRESSO_API_KEY` temporarily in `tox.ini` to run these tests against a
real Agresso instance.

Running these may take some time depending on how fast Agresso feels like
responding.
"""

import os
from unittest.mock import patch

import pytest

from agresso.service import (
    account_name,
    get_budget,
    get_budget_descriptions,
    get_general_ledger,
    get_user_log_contractor_invoices,
    get_workflow_comment_parked,
    get_workflow_contrator_invoices,
)
from test.util import is_csv_serializable


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_general_ledger():
    with patch("agresso.client._api_key") as api_key:
        api_key.return_value = os.environ["AGRESSO_API_KEY"]
        data = get_general_ledger(2024)
    assert isinstance(data, list)
    assert is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_workflow_contrator_invoices():
    with patch("agresso.client._api_key") as api_key:
        api_key.return_value = os.environ["AGRESSO_API_KEY"]
        data = get_workflow_contrator_invoices()
    assert isinstance(data, list)
    assert is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_user_log_contrator_invoices():
    with patch("agresso.client._api_key") as api_key:
        api_key.return_value = os.environ["AGRESSO_API_KEY"]
        data = get_user_log_contractor_invoices()
    assert isinstance(data, list)
    assert is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_workflow_comment_parked():
    with patch("agresso.client._api_key") as api_key:
        api_key.return_value = os.environ["AGRESSO_API_KEY"]
        data = get_workflow_comment_parked()
    assert isinstance(data, list)
    assert is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_budget():
    with patch("agresso.client._api_key") as api_key:
        api_key.return_value = os.environ["AGRESSO_API_KEY"]
        data = get_budget(2024)
    assert isinstance(data, list)
    assert is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_get_budget_descriptions():
    with patch("agresso.client._api_key") as api_key:
        api_key.return_value = os.environ["AGRESSO_API_KEY"]
        data = get_budget_descriptions(2024)
    assert isinstance(data, list)
    assert is_csv_serializable(data)


@pytest.mark.skipif("AGRESSO_API_KEY" not in os.environ, reason="missing API key")
def test_account_name():
    with patch("agresso.client._api_key") as api_key:
        api_key.return_value = os.environ["AGRESSO_API_KEY"]
        assert account_name("00100") == "Lønn faste stillinger (HR-O)"
