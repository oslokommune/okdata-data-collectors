# List of tables to import from Statistikkbanken. A new dataset is created
# automatically if it doesn't already exist.

# The available tables can be explored at:
# https://statistikkbanken.oslo.kommune.no/statbank/pxweb/no/db/1

# The base URL for the API is:
# https://statistikkbanken.oslo.kommune.no:443/statbank/sq/

DATASETS = [
    {
        "table_id": "BEF002",
        "title": "Folkemengden etter kjønn og aldersgrupper (B)",
        "query_id": "e4f4f8bb-ecff-4b62-82aa-f64d0bc12bb8",
    },
    {
        "table_id": "BEF002",
        "title": "Folkemengden etter kjønn og aldersgrupper (D)",
        "query_id": "7e19154e-faa3-439c-83a8-0f5fddb8cd13",
    },
    {
        "table_id": "BEF035",
        "title": "Befolkningsframskrivingen for 2025-2050 for alder 0-19 (D)",
        "query_id": "1bb21a58-3f54-48d1-8c5a-1399f44a3647",
    },
    {
        "table_id": "HEL010",
        "title": "Brukere av hjemmetjenester etter alder og type tjeneste (B)",
        "query_id": "3116b228-dd85-4417-b53b-fb241e1d4e16",
    },
    {
        "table_id": "UTD006",
        "title": "Barn i barnehage fordelt på alder (B)",
        "query_id": "b5335dcf-8a4a-453d-9754-b05da5a67f3e",
    },
    {
        "table_id": "UTD006",
        "title": "Barn i barnehage fordelt på alder (D)",
        "query_id": "22224a71-a006-4498-8026-cf2bf467b710",
    },
]
