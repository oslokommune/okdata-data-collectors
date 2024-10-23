"""Unit for the Barnehagefakta service.

We don't run integration tests here because it results in a lot of calls
towards the Barnehagefakta API.
"""

from unittest import mock

from barnehagefakta.service import _kindergarten_details


@mock.patch("barnehagefakta.service.barnehagefakta_barnehage_by_orgnr")
def test_kindergarten_details(barnehagefakta_barnehage_by_orgnr, kindergarten):
    barnehagefakta_barnehage_by_orgnr.return_value = kindergarten

    assert _kindergarten_details("888496092") == {
        "id": "de368ed6-e544-4a1c-b64a-c3f5285a1276",
        "alder": "1 - 2",
        "antallAnsatteFra": 1,
        "antallAnsatteTil": 4,
        "eierform": "Privat",
        "erAktiv": True,
        "erBarnehage": True,
        "erBarnehageEier": False,
        "erPrivatBarnehage": True,
        "adresselinje": "Kryssveien 10b",
        "postnr": "0583",
        "url": None,
        "koordinatLat": 59.93608,
        "koordinatLng": 10.8196,
        "malform": "Bokmål",
        "navn": "Maurtua Familiebarnehage",
        "orgnr": "888496092",
        "antallBarn": 4,
        "antallBarnPerAnsatt": None,
        "antallBarnPerBarnehagelaerer": None,
        "andelAnsatteMedBarneOgUngdomsarbeiderfag": 0.0,
        "andelAnsatteBarnehagelarer": 11.5,
        "andelAnsatteTilsvarendeBarnehagelaerer": 0.0,
        "andelAnsatteMedAnnenHoyereUtdanning": 88.5,
        "andelAnsatteMedAnnenFagarbeiderutdanning": 0.0,
        "andelAnsatteMedAnnenBakgrunn": 0.0,
        "andelAnsatteMedAnnenPedagogiskUtdanning": 0.0,
        "lekeOgOppholdsarealPerBarn": None,
        "andelBarnehagerSomOppfyllerPedagognormen": None,
        "andelBarnehagerSomIkkeOppfyllerPedagognormen": None,
        "andelBarnehagerSomOppfyllerPedagognormenMedDispensasjon": None,
        "foreldreundersokelsenUteOgInneMiljo": 5.0,
        "foreldreundersokelsenBarnetsUtvikling": None,
        "foreldreundersokelsenBarnetsTrivsel": 5.0,
        "foreldreundersokelsenInformasjon": 5.0,
        "foreldreundersokelsenTilfredshet": 5.0,
        "foreldreundersokelsenAntallInviterte": 7,
        "foreldreundersokelsenAntallBesvarte": 5,
        "foreldreundersokelsenSvarprosent": 71.4,
        "foreldreundersokelsenArgang": "2023",
        "kostpenger": 0.0,
        "type": "Familiebarnehage",
        "pedagogiskProfil": None,
        "apningstidFra": "07:30",
        "apningstidTil": "16:30",
        "oppfyllerPedagognorm": None,
        "totalAntallKvadratmeter": None,
        "urlTilSoknadOmBarnehageplass": "http://www.oslo.kommune.no/",
    }
