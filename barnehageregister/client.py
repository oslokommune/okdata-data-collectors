import requests

from common.util import getenv


def nbr_enhet_by_organisasjonsnummer(organisasjonsnummer):
    """Get kindergarten details by organisasjonsnummer from NBR."""
    res = requests.get(
        f"{getenv('BARNEHAGEREGISTER_BASE_URL')}/enhet/{organisasjonsnummer}"
    )
    res.raise_for_status()
    return res.json()


def nbr_enheter_by_kommunenummer(kommunenummer):
    """Get kindergartens by municipality number from NBR."""
    res = requests.get(
        f"{getenv('BARNEHAGEREGISTER_BASE_URL')}/enheter/kommune/{kommunenummer}"
    )
    res.raise_for_status()
    return res.json()
