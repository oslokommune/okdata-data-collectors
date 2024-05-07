def create_test_case(requested_kpis, kpis):
    kpi_responses = {kpi["kpi_id"]: _create_kpi_response(**kpi) for kpi in kpis}

    get_datasets_response = [
        _create_dataset_response(**kpi) for kpi in kpis if kpi["dataset_exists"]
    ]

    create_dataset_respoonses = [
        _create_dataset_response(**kpi) for kpi in kpis if not kpi["dataset_exists"]
    ]

    return (
        requested_kpis,
        kpi_responses,
        get_datasets_response,
        create_dataset_respoonses,
    )


def _create_kpi_response(kpi_id, name, description, parent, value_count, **kwargs):
    return (
        {
            "id": kpi_id,
            "name": name,
            "description": description,
            "parent": (
                {
                    "slug": parent.replace(" ", "-").lower(),
                    "name": parent,
                }
                if parent
                else None
            ),
            "updateFrequency": "irregular",
            "created": "2024-01-01T12:00:00.000Z",
            "createdBy": "Kamek",
        },
        [
            {
                "value": i,
                "date": "2024-02-18",
                "comment": None if i == 0 else "foo" + "o" * i,
                "created": "2024-01-02T12:00:00.000Z",
            }
            for i in range(0, value_count)
        ],
    )


def _create_dataset_response(kpi_id, name, description, parent, **kwargs):
    dataset_title = f"{parent} - {name}" if parent else name

    return {
        "Type": "Dataset",
        "Id": dataset_title.replace(" ", "-").lower(),
        "title": dataset_title,
        "description": description,
        "publisher": "Foo Corp",
        "keywords": ["kpi"],
        "objective": "test",
        "accessRights": "restricted",
        "contactPoint": {"name": "Team Foo", "email": "foo@bar.arpa"},
        "source": {"type": "file"},
        "wasDerivedFrom": {"name": "okr-tracker", "id": kpi_id},
    }
