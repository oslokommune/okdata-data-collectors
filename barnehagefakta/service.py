from barnehagefakta.client import (
    barnehagefakta_barnehage_by_orgnr,
    barnehagefakta_barnehager_by_kommunenummer,
)


def _kindergarten_details(orgnr):
    """Return details about a kindergarten based on `orgnr`."""
    k = barnehagefakta_barnehage_by_orgnr(orgnr)
    indikatorData = k["indikatorDataBarnehage"] or {}

    return {
        "id": k["id"],
        "alder": k["alder"] or None,
        "antallAnsatteFra": k["ansatte"]["antallFra"],
        "antallAnsatteTil": k["ansatte"]["antallTil"],
        "eierform": k["eierform"],
        "erAktiv": k["erAktiv"],
        "erBarnehage": k["erBarnehage"],
        "erBarnehageEier": k["erBarnehageEier"],
        "erPrivatBarnehage": k["erPrivatBarnehage"],
        "adresselinje": k["kontaktinformasjon"]["besoksAdresse"]["adresselinje"],
        "postnr": k["kontaktinformasjon"]["besoksAdresse"]["postnr"],
        "url": k["kontaktinformasjon"]["url"] or None,
        "koordinatLat": k["koordinatLatLng"][0],
        "koordinatLng": k["koordinatLatLng"][1],
        "malform": k["malform"]["malformNavn"],
        "navn": k["navn"],
        "orgnr": k["orgnr"],
        "antallBarn": indikatorData.get("antallBarn"),
        "antallBarnPerAnsatt": indikatorData.get("antallBarnPerAnsatt"),
        "antallBarnPerBarnehagelaerer": indikatorData.get(
            "antallBarnPerBarnehagelaerer"
        ),
        "andelAnsatteMedBarneOgUngdomsarbeiderfag": indikatorData.get(
            "andelAnsatteMedBarneOgUngdomsarbeiderfag"
        ),
        "andelAnsatteBarnehagelarer": indikatorData.get("andelAnsatteBarnehagelarer"),
        "andelAnsatteTilsvarendeBarnehagelaerer": indikatorData.get(
            "andelAnsatteTilsvarendeBarnehagelaerer"
        ),
        "andelAnsatteMedAnnenHoyereUtdanning": indikatorData.get(
            "andelAnsatteMedAnnenHoyereUtdanning"
        ),
        "andelAnsatteMedAnnenFagarbeiderutdanning": indikatorData.get(
            "andelAnsatteMedAnnenFagarbeiderutdanning"
        ),
        "andelAnsatteMedAnnenBakgrunn": indikatorData.get(
            "andelAnsatteMedAnnenBakgrunn"
        ),
        "andelAnsatteMedAnnenPedagogiskUtdanning": indikatorData.get(
            "andelAnsatteMedAnnenPedagogiskUtdanning"
        ),
        "lekeOgOppholdsarealPerBarn": indikatorData.get("lekeOgOppholdsarealPerBarn"),
        "andelBarnehagerSomOppfyllerPedagognormen": indikatorData.get(
            "andelBarnehagerSomOppfyllerPedagognormen"
        ),
        "andelBarnehagerSomIkkeOppfyllerPedagognormen": indikatorData.get(
            "andelBarnehagerSomIkkeOppfyllerPedagognormen"
        ),
        "andelBarnehagerSomOppfyllerPedagognormenMedDispensasjon": indikatorData.get(
            "andelBarnehagerSomOppfyllerPedagognormenMedDispensasjon"
        ),
        "foreldreundersokelsenUteOgInneMiljo": indikatorData.get(
            "foreldreundersokelsenUteOgInneMiljo"
        ),
        "foreldreundersokelsenBarnetsUtvikling": indikatorData.get(
            "foreldreundersokelsenBarnetsUtvikling"
        ),
        "foreldreundersokelsenBarnetsTrivsel": indikatorData.get(
            "foreldreundersokelsenBarnetsTrivsel"
        ),
        "foreldreundersokelsenInformasjon": indikatorData.get(
            "foreldreundersokelsenInformasjon"
        ),
        "foreldreundersokelsenTilfredshet": indikatorData.get(
            "foreldreundersokelsenTilfredshet"
        ),
        "foreldreundersokelsenAntallInviterte": indikatorData.get(
            "foreldreundersokelsenAntallInviterte"
        ),
        "foreldreundersokelsenAntallBesvarte": indikatorData.get(
            "foreldreundersokelsenAntallBesvarte"
        ),
        "foreldreundersokelsenSvarprosent": indikatorData.get(
            "foreldreundersokelsenSvarprosent"
        ),
        "foreldreundersokelsenArgang": indikatorData.get("foreldreundersokelsenArgang"),
        "kostpenger": k["kostpenger"],
        "type": k["type"],
        "pedagogiskProfil": k["pedagogiskProfil"][0] if k["pedagogiskProfil"] else None,
        "apningstidFra": k["apningstidFra"] or None,
        "apningstidTil": k["apningstidTil"] or None,
        "oppfyllerPedagognorm": k["oppfyllerPedagognorm"] or None,
        "totalAntallKvadratmeter": k["totalAntallKvadratmeter"],
        "urlTilSoknadOmBarnehageplass": k["urlTilSoknadOmBarnehageplass"],
    }


def kindergartens_in_oslo():
    return [
        _kindergarten_details(k["orgnr"])
        for k in barnehagefakta_barnehager_by_kommunenummer("0301")
    ]
