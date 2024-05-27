"""Integration tests for the Statistikkbanken client.

Set `RUN_TESTS` temporarily to true run these tests against the real
Statistikkbanken API.
"""

import csv

import pytest

from statistikkbanken.client import query_statistikkbanken
from statistikkbanken.config import DATASETS

RUN_TESTS = False


def _looks_like_csv(data):
    """Return true if `data` looks like CSV from Statistikkbanken.

    In particular that the dataset uses tab as its delimiter.
    """
    return len(data) > 0 and csv.Sniffer().sniff(data[:1024]).delimiter == "\t"


@pytest.mark.skipif(not RUN_TESTS, reason="RUN_TESTS is false")
def test_query_statistikkbanken():
    for dataset in DATASETS:
        assert _looks_like_csv(query_statistikkbanken(dataset["query_id"]))
