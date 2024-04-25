from agresso.service_helpers import (
    _enrich_result,
    _matches_filter,
    enrich_results,
    filter_results,
    remove_columns,
    rename_columns,
    simple_enricher,
)


def test_matches_filter():
    filters = {"_recno": "^1$", "account": "^2.+$"}
    assert _matches_filter({"_recno": "1", "account": "123"}, filters)
    assert _matches_filter({"_recno": "0", "account": "234"}, filters)
    assert _matches_filter({"_recno": 1, "account": 234}, filters)
    assert not _matches_filter({"_recno": "0", "account": "123"}, filters)


def test_filter_results():
    results = [
        {"_recno": "1", "account": "123"},
        {"_recno": "0", "account": "234"},
        {"_recno": "0", "account": "123"},
    ]
    filters = {"_recno": "^1$", "account": "^2.+$"}
    assert filter_results(results, filters) == [{"_recno": "0", "account": "123"}]


def test_enrich_result():
    assert _enrich_result(0, [lambda x: x + 1, lambda y: y + 2]) == 3


def test_enrich_results():
    assert enrich_results([0, 1, 2], [lambda x: x + 1, lambda y: y + 2]) == [3, 4, 5]


def test_simple_enricher():
    e = simple_enricher("a", "b", lambda x: x + "y")
    assert e({"a": "", "c": "x"}) == {"a": "", "b": "", "c": "x"}
    assert e({"a": "x"}) == {"a": "x", "b": "xy"}


def test_rename_columns():
    assert rename_columns([], {}) == []
    assert rename_columns([], {"aa": "a"}) == []
    assert rename_columns([{"a": 1, "b": 2}, {"a": 3, "b": 4}], {}) == [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
    ]
    assert rename_columns(
        [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}], {"aa": "a", "bb": "b"}
    ) == [{"aa": 1, "bb": 2, "c": 3}, {"aa": 4, "bb": 5, "c": 6}]


def test_remove_columns():
    assert remove_columns([], {}) == []
    assert remove_columns([], ["a"]) == []
    assert remove_columns([{"a": 1, "b": 2}, {"a": 3, "b": 4}], {}) == [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
    ]
    assert remove_columns(
        [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}], ["a", "b"]
    ) == [{"c": 3}, {"c": 6}]
