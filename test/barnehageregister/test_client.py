"""Integration tests for the Nasjonalt barnehageregister (NBR) client.

Set `RUN_INTEGRATION_TESTS` temporarily to true run these tests against the real NBR API.
"""

import json

import pytest


from barnehageregister.client import (
    nbr_enhet_by_organisasjonsnummer,
    nbr_enheter_by_kommunenummer,
)

RUN_INTEGRATION_TESTS = False


@pytest.mark.skipif(not RUN_INTEGRATION_TESTS, reason="RUN_INTEGRATION_TESTS is false")
def test_nbr_enhet_by_organisasjonsnummer():
    res = nbr_enhet_by_organisasjonsnummer("975315053")
    assert json.dumps(res)


@pytest.mark.skipif(not RUN_INTEGRATION_TESTS, reason="RUN_INTEGRATION_TESTS is false")
def test_nbr_enheter_by_kommunenummer():
    res = nbr_enheter_by_kommunenummer("0301")
    assert json.dumps(res)
