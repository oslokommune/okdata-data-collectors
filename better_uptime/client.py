BU_API_BASE_URL = "https://uptime.betterstack.com/api/v2"
BU_MAX_PAGES = 25


class BetterUptimeClient:
    async def monitors(self, session):
        """Return a list of all monitors by iterating all pages."""
        return await self._fetch_paginated_data(session, BU_API_BASE_URL + "/monitors")

    async def monitor_groups(self, session):
        """Return a list of all monitor groups by iterating all pages."""
        return await self._fetch_paginated_data(
            session, BU_API_BASE_URL + "/monitor-groups"
        )

    async def sla(self, session, monitor_id):
        """Return a monitor's availability summary."""
        response = await self._fetch_json(
            session, BU_API_BASE_URL + f"/monitors/{monitor_id}/sla"
        )
        return response["data"]

    async def _fetch_json(self, session, url):
        async with session.get(url) as response:
            return await response.json()

    async def _fetch_paginated_data(self, session, url):
        items = []
        current_iteration = 0
        next_page_url = url

        while next_page_url:
            current_iteration += 1
            if current_iteration == BU_MAX_PAGES:
                # Added as a precaution to prevent possible infinite loops.
                raise IterationLimitExceededError("Max page iterations reached")
            response = await self._fetch_json(session, next_page_url)
            items = items + response.get("data", [])
            next_page_url = response.get("pagination", {}).get("next")

        return items


class IterationLimitExceededError(Exception):
    pass
