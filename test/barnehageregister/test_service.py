"""Unit and integration tests for the Nasjonalt barnehageregister service.

Set `RUN_INTEGRATION_TESTS` temporarily to true run the integration tests against the real
NBR API.
"""

from unittest import mock

import pytest

from barnehageregister.service import (
    _join_key_from_dicts,
    _join_keys_from_dict,
    _kindergarten_details,
    kindergartens_in_oslo,
)
from test.util import is_csv_serializable

RUN_INTEGRATION_TESTS = False


def test_join_keys_from_dict():
    assert _join_keys_from_dict({"a": "a", "b": "b", "c": 1}, ["a", "c"]) == "a,1"


def test_join_key_from_dicts():
    assert _join_key_from_dicts([{"a": "a", "b": "b"}, {"a": 1, "b": 2}], "a") == "a,1"


@mock.patch("barnehageregister.service.nbr_enhet_by_organisasjonsnummer")
def test_kindergarten_details(nbr_enhet_by_organisasjonsnummer, kindergarten):
    nbr_enhet_by_organisasjonsnummer.return_value = kindergarten

    assert _kindergarten_details("975315053") == {
        "Organisasjonsnummer": "975315053",
        "Navn": "Maurtua barnehage",
        "Karakteristikk": None,
        "FulltNavn": "Maurtua barnehage",
        "Adresse": "Hjalmar Johansens gate 8",
        "Postnummer": "4019",
        "Koordinat": "5.72564,58.95041",
        "Internettadresse": "",
        "Maalform": "Bokmål",
        "Organisasjonsform": "Underenhet til næringsdrivende og offentlig sektor",
        "Naeringskoder": "88.911",
        "Hjelpeenhetskode": None,
        "Utgaattype": "Ingen utgåttype",
        "ErAktiv": True,
        "ErBarnehage": True,
        "ErBarnehageEier": False,
        "ErOffentligBarnehage": True,
        "ErPrivatBarnehage": False,
        "ErInaktivIBasil": True,
        "AntallBarn": 36,
        "AntallAnsatte": 9,
        "AlderstrinnFra": 1,
        "AlderstrinnTil": 5,
        "Barnehagekategorier": "Kommunal barnehage,Offentlig barnehage",
        "OppstartsEllerStiftelsesdato": "1989-01-02T00:00:00+01:00",
        "DatoEndret": "2024-02-14T07:35:10.39+01:00",
    }


@pytest.mark.skipif(not RUN_INTEGRATION_TESTS, reason="RUN_INTEGRATION_TESTS is False")
def test_kindergartens_in_oslo():
    data = kindergartens_in_oslo()

    assert isinstance(data, list)
    assert is_csv_serializable(data)
