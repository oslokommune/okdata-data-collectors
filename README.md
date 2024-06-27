# okdata-data-collectors

Data collector jobs for the Origo dataplatform.

The following sources are currently implemented:

- `agresso`: Economy data from Agresso.
- `better_uptime`: Service uptime data from Better Stack.
- `measurements`: Measurements (KPIs) from the OKR Tracker.

## Setup

```sh
make init
```

## Test

Tests are run using [tox](https://pypi.org/project/tox/):

```sh
make test
```

For tests and linting we use [pytest](https://pypi.org/project/pytest/),
[flake8](https://pypi.org/project/flake8/), and
[black](https://pypi.org/project/black/).

## Deploy

GitHub Actions deploys to dev and prod on push to `main`.

You can also deploy from a local machine to dev with:

```sh
make deploy
```

Or to prod with:

```sh
make deploy-prod
```
