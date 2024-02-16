from aiohttp import ClientSession

BU_API_BASE_URL = "https://uptime.betterstack.com/api/v2"
BU_MAX_PAGES = 25


class BetterUptimeClient:
    def __init__(self, access_token, raise_for_status=True):
        self.session = ClientSession(
            headers={"Authorization": f"Bearer {access_token}"},
            raise_for_status=raise_for_status,
        )

    async def monitors(self):
        """Return a list of all monitors by iterating all pages."""
        return await self._fetch_paginated_data(BU_API_BASE_URL + "/monitors")

    async def monitor_groups(self):
        """Return a list of all monitor groups by iterating all pages."""
        return await self._fetch_paginated_data(BU_API_BASE_URL + "/monitor-groups")

    async def sla(self, monitor_id):
        """Return a monitor's availability summary."""
        response = await self._fetch_json(
            f"{BU_API_BASE_URL}/monitors/{monitor_id}/sla"
        )
        return response["data"]

    async def _fetch_json(self, url):
        async with self.session.get(url) as response:
            return await response.json()

    async def _fetch_paginated_data(self, url):
        items = []
        current_iteration = 0
        next_page_url = url

        while next_page_url:
            current_iteration += 1
            if current_iteration == BU_MAX_PAGES:
                # Added as a precaution to prevent possible infinite loops.
                raise IterationLimitExceededError("Max page iterations reached")
            response = await self._fetch_json(next_page_url)
            items = items + response.get("data", [])
            next_page_url = response.get("pagination", {}).get("next")

        return items

    async def __aenter__(self):
        return self

    async def __aexit__(self, *error_info):
        await self.session.close()


class IterationLimitExceededError(Exception):
    pass
