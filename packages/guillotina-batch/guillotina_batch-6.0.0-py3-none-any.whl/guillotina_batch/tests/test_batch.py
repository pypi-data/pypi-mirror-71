import json
import pytest


pytestmark = pytest.mark.asyncio


async def test_batch_get_data(container_requester):
    """Check a value from registry."""
    async with container_requester as requester:
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar1"}),
        )
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar2"}),
        )
        response, _ = await requester(
            "POST",
            "/db/guillotina/@batch",
            data=json.dumps(
                [
                    {"method": "GET", "endpoint": "foobar1"},
                    {"method": "GET", "endpoint": "foobar2"},
                ]
            ),
        )
        assert len(response) == 2
        assert response[1]["body"]["@name"] == "foobar2"


async def test_batch_validates_parameters(container_requester):
    async with container_requester as requester:
        _, status = await requester(
            "POST",
            "/db/guillotina/@batch",
            data=json.dumps(
                [
                    {"endpoint": "foobar1"},  # method key missing
                    {"method": "GET", "endpoint": "foobar2"},
                ]
            ),
        )
        assert status == 412


async def test_edit_data(container_requester):
    """Check a value from registry."""
    async with container_requester as requester:
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar1"}),
        )
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar2"}),
        )
        response, _ = await requester(
            "POST",
            "/db/guillotina/@batch",
            data=json.dumps(
                [
                    {
                        "method": "PATCH",
                        "endpoint": "foobar1",
                        "payload": {"title": "Foobar1 changed"},
                    },
                    {
                        "method": "PATCH",
                        "endpoint": "foobar2",
                        "payload": {"title": "Foobar2 changed"},
                    },
                ]
            ),
        )
        response, _ = await requester(
            "POST",
            "/db/guillotina/@batch",
            data=json.dumps(
                [
                    {"method": "GET", "endpoint": "foobar1"},
                    {"method": "GET", "endpoint": "foobar2"},
                ]
            ),
        )
        assert len(response) == 2
        assert response[0]["body"]["title"] == "Foobar1 changed"
        assert response[1]["body"]["title"] == "Foobar2 changed"


async def test_edit_sharing_data(container_requester):
    """Check a value from registry."""
    async with container_requester as requester:
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar1"}),
        )
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar2"}),
        )
        response, _ = await requester(
            "POST",
            "/db/guillotina/@batch",
            data=json.dumps(
                [
                    {
                        "method": "POST",
                        "endpoint": "foobar1/@sharing",
                        "payload": {
                            "prinperm": [
                                {
                                    "principal": "user1",
                                    "permission": "guillotina.AccessContent",
                                    "setting": "AllowSingle",
                                }
                            ]
                        },
                    },
                    {
                        "method": "POST",
                        "endpoint": "foobar2/@sharing",
                        "payload": {
                            "prinperm": [
                                {
                                    "principal": "user1",
                                    "permission": "guillotina.AccessContent",
                                    "setting": "AllowSingle",
                                }
                            ]
                        },
                    },
                ]
            ),
        )
        response, _ = await requester(
            "POST",
            "/db/guillotina/@batch",
            data=json.dumps(
                [
                    {"method": "GET", "endpoint": "foobar1/@sharing"},
                    {"method": "GET", "endpoint": "foobar2/@sharing"},
                ]
            ),
        )
        assert len(response) == 2
        assert (
            response[0]["body"]["local"]["prinperm"]["user1"][
                "guillotina.AccessContent"
            ]
            == "AllowSingle"
        )
        assert (
            response[1]["body"]["local"]["prinperm"]["user1"][
                "guillotina.AccessContent"
            ]
            == "AllowSingle"
        )


async def test_querying_permissions(container_requester):
    async with container_requester as requester:
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar1"}),
        )
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar2"}),
        )

        response, _ = await requester(
            "POST",
            "/db/guillotina/@batch",
            data=json.dumps(
                [
                    {
                        "method": "GET",
                        "endpoint": "foobar1/@canido?permission=guillotina.ChangePermissions",
                    },
                    {
                        "method": "GET",
                        "endpoint": "foobar2/@canido?permission=guillotina.ChangePermissions",
                    },
                ]
            ),
        )
        assert len(response) == 2
        for resp in response:
            assert resp["status"] == 200 and resp["success"]


async def test_batch_error_returned_in_individual_response_items(container_requester):
    async with container_requester as requester:
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar1"}),
        )
        await requester(
            "POST",
            "/db/guillotina",
            data=json.dumps({"@type": "Item", "id": "foobar2"}),
        )
        response, status = await requester(
            "POST",
            "/db/guillotina/@batch",
            data=json.dumps(
                [
                    {"method": "GET", "endpoint": "foobar1"},
                    {"method": "GET", "endpoint": "foobar2"},
                    {
                        "method": "POST",
                        "endpoint": "/foobar2/@duplicate",
                        "payload": {
                            "new_id": "foobar1",  # <-- Generates error: ids collide
                            "destination": "/",
                        },
                    },
                ]
            ),
        )
        assert status == 200
        assert len(response) == 3
        assert not response[2]["success"]
        assert response[2]["status"] == 412


async def test_batch_internal_error_on_individual_response_is_returned_properly(
    container_requester,
):
    async with container_requester as requester:
        resp, status = await requester(
            "POST",
            "/db/guillotina/@batch",
            data=json.dumps(
                [
                    {
                        "method": "POST",
                        "endpoint": "@respond",
                        "payload": {"exception": True},
                    },
                    {
                        "method": "POST",
                        "endpoint": "@respond",
                        "payload": {"exception": False},
                    },
                ]
            ),
        )
        assert status == 200
        assert resp[0]["status"] == 500
        assert resp[1]["status"] == 200
