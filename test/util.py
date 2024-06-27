import types


def _all_keys_match(dicts):
    """Return true if all `dicts` have the same keys."""
    keys = dicts[0].keys()
    return all([keys == d.keys() for d in dicts[1:]])


def _all_values_are_simple(dicts):
    """Return true if all values in `dicts` are "simple".

    We consider "simple types" as int, float, str, and NoneType.
    """
    return all(
        [
            all([isinstance(v, int | float | str | types.NoneType) for v in d.values()])
            for d in dicts
        ]
    )


def is_csv_serializable(data):
    """Return true if `data` is CSV serializable by our JSON->CSV pipeline.

    In particular, check that all the dicts in `data` contain the same keys and
    have simple (non-compound) values.
    """
    if len(data) == 0:
        return True

    return _all_keys_match(data) and _all_values_are_simple(data)
