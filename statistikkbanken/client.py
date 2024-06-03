import requests

from common.util import getenv


def query_statistikkbanken(query_id):
    """Query Statistikkbanken and return the raw CSV response."""
    res = requests.get(f"{getenv('STATISTIKKBANKEN_BASE_URL')}/{query_id}")
    res.raise_for_status()
    return res.text
