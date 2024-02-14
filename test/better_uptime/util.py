def create_monitor(
    monitor_id,
    name,
    url,
    group_id=None,
    paused=False,
):
    return (
        {
            "id": str(monitor_id),
            "type": "monitor",
            "attributes": {
                "url": url,
                "pronounceable_name": name,
                "monitor_type": "status",
                "monitor_group_id": group_id,
                "last_checked_at": "2024-02-12T13:23:19.000Z",
                "status": "up",
                "http_method": "get",
                "created_at": "2024-02-06T13:47:28.555Z",
                "updated_at": "2024-02-09T09:40:34.744Z",
                "paused_at": "2024-02-09T09:40:34.744Z" if paused else None,
                "paused": paused,
                # ...
            },
        },
        {
            "id": str(monitor_id),
            "type": "monitor_sla",
            "attributes": {
                "availability": 100.0,
                "total_downtime": 0,
                "number_of_incidents": 0,
                "longest_incident": 0,
                "average_incident": 0,
            },
        },
    )


def create_group(group_id, name):
    return {
        "id": str(group_id),
        "type": "monitor_group",
        "attributes": {
            "name": name,
            "created_at": "2024-02-06T14:04:23.862Z",
            "updated_at": "2024-02-06T14:04:23.862Z",
            "sort_index": None,
            "paused": False,
        },
    }


def create_response_data(monitors=[], groups=[], per_page=5):
    return {
        "monitors": list(
            _paginated_response("monitors", [m[0] for m in monitors], per_page)
        ),
        "sla": {m[1]["id"]: m[1] for m in monitors},
        "groups": list(_paginated_response("monitor-groups", groups, per_page)),
        "per_page": per_page,
    }


def _chunk_items(items, per_page):
    for i in range(0, len(items), per_page):
        yield items[i : i + per_page]


def _paginated_response(path, items, per_page):
    page_url = "https://uptime.betterstack.com/api/v2/" + path
    item_groups = list(_chunk_items(items, per_page))
    page_count = len(item_groups)

    if not items:
        yield {
            "data": [],
            "pagination": {
                "first": f"{page_url}?page=1",
                "last": f"{page_url}?page=1",
                "prev": None,
                "next": None,
            },
        }

    for page_num, items in enumerate(item_groups, 1):
        has_next_page = page_num < page_count
        has_prev_page = page_num > 1

        yield {
            "data": items,
            "pagination": {
                "first": f"{page_url}?page={page_num}",
                "last": f"{page_url}?page={page_count}",
                "prev": (f"{page_url}?page={page_num - 1}" if has_prev_page else None),
                "next": (f"{page_url}?page={page_num + 1}" if has_next_page else None),
            },
        }
