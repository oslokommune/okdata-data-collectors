from datetime import datetime, timedelta

import disruptive


class DisruptiveClient:
    def __init__(
        self, service_account_email, service_account_key_id, service_account_secret
    ):
        self.service_account = disruptive.Auth.service_account(
            email=service_account_email,
            key_id=service_account_key_id,
            secret=service_account_secret,
        )

    def get_project(self, project_id):
        return disruptive.Project.get_project(project_id, auth=self.service_account)

    def list_devices(self, project_id):
        return disruptive.Device.list_devices(project_id, auth=self.service_account)

    def get_events(self, project, device):
        events = disruptive.EventHistory.list_events(
            device.device_id,
            project.project_id,
            event_types=[disruptive.events.TEMPERATURE],
            # Maximum is ~a month back in time
            start_time=datetime.now() - timedelta(days=32),
            auth=self.service_account,
        )
        return [
            {
                "project_id": project.project_id,
                "project_name": project.display_name,
                "device_id": device.device_id,
                "device_name": device.display_name,
                "timestamp": e.data.timestamp,
                "temperature": e.data.celsius,
            }
            for e in events
        ]
