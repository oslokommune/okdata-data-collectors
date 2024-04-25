"""Integration tests for the SSB API collector.

Set `RUN_TESTS` temporarily to true run these tests against the real SSB API.
"""

import csv

import pytest

from ssb.client import get_dataset
from ssb.handlers import DATASETS

RUN_TESTS = False


def _looks_like_csv(data):
    """Return true if `data` looks like CSV from SSB.

    In particular, SSB uses `;` as their delimiter.
    """
    return len(data) > 0 and csv.Sniffer().sniff(data[:1024]).delimiter == ";"


@pytest.mark.skipif(not RUN_TESTS, reason="RUN_TESTS is false")
def test_get_datasets():
    for ssb_dataset_id, dataset_id in DATASETS.items():
        assert _looks_like_csv(get_dataset(ssb_dataset_id))
