from operator import itemgetter

from barnehageregister.client import (
    nbr_enhet_by_organisasjonsnummer,
    nbr_enheter_by_kommunenummer,
)


def _join_keys_from_dict(d, keys):
    """Return all `keys` from the dict `d` joined by ','."""
    return ",".join([str(d[k]) for k in keys])


def _join_key_from_dicts(dicts, key):
    """Return `key` from all `dicts` joined by ','."""
    return ",".join([str(d[key]) for d in dicts])


def _kindergarten_details(organisasjonsnummer):
    """Return details about a kindergarten based on `organisasjonsnummer`."""
    k = nbr_enhet_by_organisasjonsnummer(organisasjonsnummer)

    return {
        "Organisasjonsnummer": k["Organisasjonsnummer"],
        "Navn": k["Navn"],
        "Karakteristikk": k["Karakteristikk"],
        "FulltNavn": k["FulltNavn"],
        "Adresse": k["Beliggenhetsadresse"]["Adresse"],
        "Postnummer": k["Beliggenhetsadresse"]["Postnummer"],
        "Koordinat": _join_keys_from_dict(k["Koordinat"], ["Lengdegrad", "Breddegrad"]),
        "Internettadresse": k["Internettadresse"],
        "Maalform": k["Maalform"]["Navn"],
        "Organisasjonsform": k["Organisasjonsform"]["Navn"],
        "Naeringskoder": _join_key_from_dicts(
            sorted(k["Naeringskoder"], key=itemgetter("Prioritet")), "Kode"
        ),
        "Hjelpeenhetskode": k["Hjelpeenhetskode"],
        "Utgaattype": k["Utgaattype"]["Navn"],
        "ErAktiv": k["ErAktiv"],
        "ErBarnehage": k["ErBarnehage"],
        "ErBarnehageEier": k["ErBarnehageEier"],
        "ErOffentligBarnehage": k["ErOffentligBarnehage"],
        "ErPrivatBarnehage": k["ErPrivatBarnehage"],
        "ErInaktivIBasil": k["ErInaktivIBasil"],
        "AntallBarn": k["AntallBarn"],
        "AntallAnsatte": k["AntallAnsatte"],
        "AlderstrinnFra": k["AlderstrinnFra"],
        "AlderstrinnTil": k["AlderstrinnTil"],
        "Barnehagekategorier": _join_key_from_dicts(k["Barnehagekategorier"], "Navn"),
        "OppstartsEllerStiftelsesdato": k["OppstartsEllerStiftelsesdato"],
        "DatoEndret": k["DatoEndret"],
    }


def kindergartens_in_oslo():
    return [
        _kindergarten_details(k["Organisasjonsnummer"])
        for k in nbr_enheter_by_kommunenummer("0301")["EnhetListe"]
    ]
