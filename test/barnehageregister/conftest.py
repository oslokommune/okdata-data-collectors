import pytest


@pytest.fixture
def kindergarten():
    return {
        "Organisasjonsnummer": "975315053",
        "Navn": "Maurtua barnehage",
        "Karakteristikk": None,
        "FulltNavn": "Maurtua barnehage",
        "Fylke": {
            "Fylkesnummer": "11",
            "Navn": "Rogaland",
            "Organisasjonsnummer": "971045698",
            "StatsforvalterOrganisasjonsnummer": "974763230",
        },
        "Kommune": {
            "Navn": "Stavanger",
            "Kommunenummer": "1103",
            "Organisasjonsnummer": "964965226",
            "ErNedlagt": False,
            "Fylkesnummer": "11",
            "Kostragruppe": {"Id": 12, "Navn": "KOSTRA-gruppe 12"},
        },
        "Beliggenhetsadresse": {
            "Adresse": "Hjalmar Johansens gate 8",
            "Postnummer": "4019",
            "Poststed": "STAVANGER",
            "Land": "Norge",
        },
        "Postadresse": {
            "Adresse": "Postboks 355",
            "Postnummer": "4068",
            "Poststed": "STAVANGER",
            "Land": "Norge",
        },
        "Koordinat": {
            "Lengdegrad": 5.72564,
            "Breddegrad": 58.95041,
            "Zoom": 12,
            "GeoKilde": "GeoNorge",
        },
        "Internettadresse": "",
        "Maalform": {"Id": "B", "Navn": "Bokmål"},
        "Organisasjonsform": {
            "Id": "BEDR",
            "Navn": "Underenhet til næringsdrivende og offentlig sektor",
        },
        "Naeringskoder": [
            {"Prioritet": 1, "Kode": "88.911", "Navn": "Barnehager", "Versjon": "2007"}
        ],
        "Hjelpeenhetskode": None,
        "Utgaattype": {"Id": "A", "Navn": "Ingen utgåttype"},
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
        "Barnehagekategorier": [
            {"Id": "19", "Navn": "Kommunal barnehage"},
            {"Id": "18", "Navn": "Offentlig barnehage"},
        ],
        "ForeldreRelasjoner": [
            {
                "Enhet": {
                    "Organisasjonsnummer": "964965226",
                    "Navn": "Stavanger kommune",
                },
                "Relasjonstype": {"Id": "6", "Navn": "Eierstruktur"},
            },
            {
                "Enhet": {
                    "Organisasjonsnummer": "964965226",
                    "Navn": "Stavanger kommune",
                },
                "Relasjonstype": {"Id": "7", "Navn": "Tilsynsstruktur"},
            },
            {
                "Enhet": {
                    "Organisasjonsnummer": "964965226",
                    "Navn": "Stavanger kommune",
                },
                "Relasjonstype": {"Id": "10", "Navn": "Administrativ struktur"},
            },
            {
                "Enhet": {
                    "Organisasjonsnummer": "983518648",
                    "Navn": "Stavanger kommune Oppvekst og Utdanning",
                },
                "Relasjonstype": {"Id": "9", "Navn": "Tilknytningsstruktur"},
            },
        ],
        "BarnRelasjoner": [],
        "OppstartsEllerStiftelsesdato": "1989-01-02T00:00:00+01:00",
        "DatoEndret": "2024-02-14T07:35:10.39+01:00",
    }
