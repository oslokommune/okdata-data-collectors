import functools

from agresso.client import get_results, get_results_for_year, get_term_description
from agresso.service_helpers import (
    enrich_results,
    filter_results,
    remove_columns,
    rename_columns,
    simple_enricher,
)
from common.util import getenv


###
# Helpers to fetch term descriptions from the Agresso API for enriching other
# results. The values as cached to avoid hitting the API unnecessarily.
###


@functools.cache
def account_name(account_id):
    return get_term_description("ART", account_id)


@functools.cache
def contractor_name(contractor_id):
    return get_term_description("LEVNR", contractor_id)


@functools.cache
def cost_center_name(cost_center_id):
    return get_term_description("KOSTSTED", cost_center_id)


@functools.cache
def project_name(project_id):
    return get_term_description("PROSJEKT", project_id)


###
# The actual report fetchers; each function corresponds to a dataset/report.
###


# Dataset `hovedbok-gl11-{year}`
def get_general_ledger(year):
    def _enrich_voucher_url(row):
        row["voucher_url"] = (
            f"{getenv('AGRESSO_PDF_BASE_URL')}/{row['voucher_no']}"
            if row["voucher_type"] in ["EF", "I2"]
            else ""
        )
        return row

    return remove_columns(
        rename_columns(
            enrich_results(
                filter_results(
                    get_results_for_year("81656", year, skip_future=True),
                    {
                        # Irrelevant rows
                        "_recno": "^1$",
                        # Balance accounts
                        "account": "^2.+$",
                    },
                ),
                [
                    _enrich_voucher_url,
                    simple_enricher("account", "Kontonavn", account_name),
                    simple_enricher("apar_id", "Leverandørnavn", contractor_name),
                    simple_enricher("dim_1", "Koststedsnavn", cost_center_name),
                    simple_enricher("dim_4", "Prosjektnavn", project_name),
                ],
            ),
            {
                "Valutabeløp": "cur_amount",
                "Valuta": "currency",
                "Beskrivelse": "description",
                "Koststed": "dim_1",
                "Funksjon": "dim_2",
                "AnleggRessursnummer": "dim_3",
                "Prosjekt": "dim_4",
                "SistOppdatert": "last_update",
                "Periode": "period",
                "Avgiftskode": "tax_code",
                "Bilagsdato": "voucher_date",
                "Bilagsnummer": "voucher_no",
                "Bilagstype": "voucher_type",
                "Bilagsurl": "voucher_url",
            },
        ),
        ["_recno"],
    )


# Dataset `arbeidsflyt-levfakt-wf68`
def get_workflow_contrator_invoices():
    return filter_results(get_results("88112"), {"_recno": "^1$"})


# Dataset `brukerlog-levfakt-wF80`
def get_user_log_contractor_invoices():
    return get_results("86289")


# Dataset `arbeidsflytkommentar-parkert`
def get_workflow_comment_parked():
    return remove_columns(get_results("81881"), ["_recno"])


# Dataset `budsjett-{year}`
def get_budget(year):
    return remove_columns(
        rename_columns(
            enrich_results(
                filter_results(get_results_for_year("81882", year), {"_recno": "^1$"}),
                [
                    simple_enricher("dim1", "Kontonavn", account_name),
                    simple_enricher("dim2", "Koststedsnavn", cost_center_name),
                    simple_enricher("dim4", "Prosjektnavn", project_name),
                ],
            ),
            {
                "Konto": "dim1",
                "Koststed": "dim2",
                "Funksjon": "dim3",
                "Prosjekt": "dim4",
            },
        ),
        ["_recno"],
    )


# Dataset `budsjett-beskrivelse-{year}`
def get_budget_descriptions(year):
    return remove_columns(
        filter_results(get_results_for_year("84600", year), {"_recno": "^1$"}),
        ["_recno"],
    )
