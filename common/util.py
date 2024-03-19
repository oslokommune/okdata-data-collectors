import os
import csv


def getenv(name):
    """Return the environment variable named `name`.

    Raise `OSError` if it's unset.
    """
    env = os.getenv(name)

    if env is None:
        raise OSError(f"Environment variable {name} is not set")

    return env


def write_dict_to_csv(filename, data, fieldnames, **kwargs):
    with open(filename, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, **kwargs)
        writer.writeheader()

        for row in data:
            writer.writerow(row)

        return csv_file
