import csv

from aws_xray_sdk.core import patch_all, xray_recorder
from okdata.aws.logging import logging_wrapper
from okdata.aws.ssm import get_secret

from common.dataplatform import upload_dataset
from common.util import getenv
from okdata_disruptive.client import DisruptiveClient

patch_all()

# Projects to import data from.
PROJECT_IDS = [
    "c0vnqtm0c7bet3vics90",  # Bydel Grorud
    "c0vnqb5v4t6ssbpguueg",  # Bydel Vestre Aker
    "c17lkka9kmt7101g0ijg",  # Hovedlager Nydalen
    "c4iudupgt1qt96jhsjp0",  # Lahaugmoen
]


@logging_wrapper
@xray_recorder.capture("import_data")
def import_data(event, context):
    disruptive_client = DisruptiveClient(
        getenv("DISRUPTIVE_SERVICE_ACCOUNT_EMAIL"),
        getenv("DISRUPTIVE_SERVICE_ACCOUNT_KEY_ID"),
        get_secret("/dataplatform/disruptive/service-account-secret"),
    )
    with open("/tmp/disruptive_data.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "project_id",
                "project_name",
                "device_id",
                "device_name",
                "timestamp",
                "temperature",
            ],
        )
        writer.writeheader()
        for project_id in PROJECT_IDS:
            project = disruptive_client.get_project(project_id)
            for device in disruptive_client.list_devices(project_id):
                for events in disruptive_client.get_events(project, device):
                    writer.writerow(events)
        upload_dataset("disruptive-test", f.name)
