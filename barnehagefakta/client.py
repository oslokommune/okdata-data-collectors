import requests

from common.util import getenv


def barnehagefakta_barnehage_by_orgnr(orgnr):
    """Get kindergarten details by org.nr. from Barnehagefakta."""
    res = requests.get(f"{getenv('BARNEHAGEFAKTA_BASE_URL')}/Barnehage/orgnr/{orgnr}")
    res.raise_for_status()
    return res.json()


def barnehagefakta_barnehager_by_kommunenummer(kommunenummer):
    """Get kindergartens by municipality number from Barnehagefakta."""
    res = requests.get(
        f"{getenv('BARNEHAGEFAKTA_BASE_URL')}/Location/kommune/{kommunenummer}"
    )
    res.raise_for_status()
    return res.json()
