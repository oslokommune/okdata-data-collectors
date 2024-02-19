import re


def _matches_filter(result, filters):
    """Return true if `result` matches any of the filters in `filters`."""
    for attr, pattern in filters.items():
        if (value := result.get(attr)) and re.match(pattern, str(value)):
            return True
    return False


def filter_results(results, filters):
    """Filter out dicts from the list `results` matching `filters`.

    `filters` is a dict mapping data keys to regexes to filter their values on.

    Example: `filters = {"foo": "^bar.*$"}` removes every dict from `results`
    that has a key "foo" whose value begins "bar".
    """
    return [res for res in results if not _matches_filter(res, filters)]


def _enrich_result(result, enrichments):
    """Return `result` after piping it through every function in `enrichments`"""
    for enrich in enrichments:
        result = enrich(result)
    return result


def enrich_results(results, enrichments):
    """Enrich every element of `results` with every function in `enrichments`"""
    return [_enrich_result(r, enrichments) for r in results]


def simple_enricher(from_field, to_field, transformer):
    """Return a function mapping `from_field` to `to_field` by `transformer`.

    `transformer` should take a single argument and return the value to use for
    `to_field` based on the value in `from_field`.
    """

    def _transformer(row):
        val = row[from_field]
        row[to_field] = "" if val == "" else transformer(val)
        return row

    return _transformer
