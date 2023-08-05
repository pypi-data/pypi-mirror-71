from guillotina import configure
from guillotina.interfaces import IFolder
from guillotina.transactions import get_tm
from guillotina.transactions import get_transaction

import json
import os
import pytest


pytestmark = pytest.mark.asyncio

DATABASE = os.environ.get("DATABASE", "DUMMY")


async def test_batch_eager_commit(container_requester):
    async with container_requester as requester:
        resp, status = await requester(
            "POST",
            "/db/guillotina/@batch?eager-commit=true",
            data=json.dumps(
                [
                    {
                        "method": "POST",
                        "endpoint": "",
                        "payload": {"@type": "Folder", "id": "folder"},
                    },
                    {
                        "method": "POST",
                        "payload": {"@type": "Item", "id": "item"},
                        "endpoint": "folder",
                    },
                    {
                        "method": "POST",
                        "payload": {"@type": "Item", "id": "item"},
                        "endpoint": "folder",
                    },
                    {
                        "method": "POST",
                        "payload": {"@type": "Item", "id": "another-item"},
                        "endpoint": "folder",
                    },
                    {"method": "GET", "endpoint": "folder/another-item"},
                ]
            ),
        )
        assert status == 200
        assert resp[0]["status"] == 201 and resp[0]["success"] is True
        assert resp[1]["status"] == 201 and resp[1]["success"] is True
        assert resp[2]["status"] == 409 and resp[2]["success"] is False
        assert resp[3]["status"] == 201 and resp[3]["success"] is True
        assert resp[4]["status"] == 200 and resp[4]["success"] is True

        resp, status = await requester("GET", "/db/guillotina/folder")
        assert status == 200

        resp, status = await requester("GET", "/db/guillotina/folder/item")
        assert status == 200


@configure.service(
    method="POST",
    name="@test-retry-logic",
    context=IFolder,
    permission="guillotina.AccessContent",
)
async def retry_logic(context, request):
    """
    First time sets 'title' and produce a conflict when the title is edited.
    Then this request should be retried automatically and finish successfuly
    """
    ob = await context.async_get("bar")

    if ob.title is None:
        # Modify field 'title' and commit change
        ob.title = "A beautiful title"
        tm = get_tm()
        txn = get_transaction()
        txn.register(ob)
        await tm.commit()

        # Simulate a conflict error to test retry logic
        await tm.begin()
        ob.title = "edit title"
        ob.__serial__ = 3242432  # should raise conflict error when tm.commit()
        txn.register(ob)

    elif ob.title == "A beautiful title":
        ob.title = "retry logic works"
        txn = get_transaction()
        txn.register(ob)

    else:
        raise Exception("Something is not working as expected")


@pytest.mark.skipif(DATABASE == "DUMMY", reason="Not for dummy db")
async def test_batch_eager_commit_conflict(container_requester):
    async with container_requester as requester:
        resp, status = await requester(
            "POST",
            "/db/guillotina/",
            data=json.dumps({"@type": "Folder", "id": "foo"}),  # type: ignore
        )
        assert status == 201

        resp, status = await requester(
            "POST",
            "/db/guillotina/foo",
            data=json.dumps({"@type": "Item", "id": "bar"}),  # type: ignore
        )
        assert status == 201

        resp, status = await requester(
            "POST",
            "/db/guillotina/@batch?eager-commit=true",
            data=json.dumps(
                [{"method": "POST", "endpoint": "foo/@test-retry-logic"}]
            ),  # type: ignore
        )
        assert status == 200
        assert resp[0]["status"] == 200

        resp, status = await requester("GET", "/db/guillotina/foo/bar")
        assert status == 200
        assert resp["title"] == "retry logic works"
