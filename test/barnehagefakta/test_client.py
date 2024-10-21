"""Integration tests for the Barnehagefakta client.

Set `RUN_INTEGRATION_TESTS` temporarily to true run these tests against the
real Barnehagefakta API.
"""

import json

import pytest

from barnehagefakta.client import (
    barnehagefakta_barnehage_by_orgnr,
    barnehagefakta_barnehager_by_kommunenummer,
)

RUN_INTEGRATION_TESTS = False


@pytest.mark.skipif(not RUN_INTEGRATION_TESTS, reason="RUN_INTEGRATION_TESTS is false")
def test_barnehagefakta_barnehage_by_orgnr():
    res = barnehagefakta_barnehage_by_orgnr("888496092")
    assert json.dumps(res)


@pytest.mark.skipif(not RUN_INTEGRATION_TESTS, reason="RUN_INTEGRATION_TESTS is false")
def test_barnehagefakta_barnehager_by_kommunenummer():
    res = barnehagefakta_barnehager_by_kommunenummer("0301")
    assert json.dumps(res)
