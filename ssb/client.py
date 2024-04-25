import requests

from common.util import getenv


def get_dataset(dataset_id):
    """Return the raw CSV dataset from SSB with ID `dataset_id`."""
    res = requests.get(f"{getenv('SSB_BASE_URL')}/dataset/{dataset_id}.csv?lang=no")
    res.raise_for_status()
    return res.text
