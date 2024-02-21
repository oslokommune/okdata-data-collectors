import functools
import json
from datetime import datetime

import requests
from okdata.aws.ssm import get_secret

from common.util import getenv


class UnknownTemplateId(ValueError):
    """Raised when trying to use an unknown template ID."""

    def __init__(self, template_id):
        super().__init__(f"Unknown template ID: {template_id}")


@functools.cache
def _api_key():
    return get_secret("/dataplatform/agresso/api-key")


def _search_criteria(template_id, replacements={}):
    """Return search criteria for template `template_id`.

    Raise `UnknownTemplateId` if the template ID is unknown.
    """
    try:
        with open(f"agresso/data/search_criteria/{template_id}.json") as f:
            search_criteria = f.read()
            for k, v in replacements.items():
                search_criteria = search_criteria.replace(k, v)
            return json.loads(search_criteria)
    except FileNotFoundError:
        raise UnknownTemplateId(template_id)


def _all_periods(year):
    """Return a list of all periods in `year`.

    The periods are on the format YYYYMM, suitable for use in the `fromValue`
    filter field in the Agresso API.
    """
    return [f"{year}{str(month).zfill(2)}" for month in range(1, 13)]


def _current_and_past_periods(year):
    """Return a list of the current and past periods in `year`.

    The periods are on the format YYYYMM, suitable for use in the `fromValue`
    filter field in the Agresso API.
    """
    now = datetime.now()

    return [
        f"{year}{str(month).zfill(2)}"
        for month in range(1, 13)
        if year < now.year or year == now.year and month <= now.month
    ]


def _get_results(template_id, search_criteria):
    res = requests.request(
        "POST",
        f"{getenv('AGRESSO_BASE_URL')}/results/{template_id}",
        headers={
            "Content-Type": "application/json",
            "apiKey": _api_key(),
        },
        json=search_criteria,
    )
    res.raise_for_status()
    return res.json()


def get_results(template_id):
    return _get_results(template_id, _search_criteria(template_id))


def get_results_for_year(template_id, year, skip_future=False):
    res = []
    periods = _current_and_past_periods(year) if skip_future else _all_periods(year)

    for period in periods:
        search_criteria = _search_criteria(template_id, {"##PERIOD##": period})
        res.extend(_get_results(template_id, search_criteria))

    return res


def get_term_description(term, value):
    template_id = "81660"
    search_criteria = _search_criteria(
        template_id, {"##ATT_NAME##": term, "##DIM_VALUE##": str(value)}
    )
    res = _get_results(template_id, search_criteria)
    return res.get("description") if isinstance(res, dict) else ""
