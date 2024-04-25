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


def rename_columns(results, name_map):
    """Rename the keys of every dict in `results` according to `name_map`.

    `name_map` should be a dict on the form:
    {
      "new_name_1": "old_name_1",
      "new_name_2": "old_name_2",
      ...
    }
    """
    for res in results:
        for to_name, from_name in name_map.items():
            res[to_name] = res[from_name]
            del res[from_name]
    return results


def remove_columns(results, columns):
    """Remove every key in `columns` from every dict in `results`"""
    for res in results:
        for col in columns:
            del res[col]
    return results
