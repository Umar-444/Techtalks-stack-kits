import pytest
from litestar.testing import AsyncTestClient
from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncTestClient(app=app) as client:
        res = await client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"
        assert data["framework"] == "litestar"
        assert data["typing"] == "strict"

@pytest.mark.asyncio
async def test_create_and_list_items():
    async with AsyncTestClient(app=app) as client:
        create_res = await client.post(
            "/api/v1/items",
            json={"title": "Cloud Server", "tenant_id": "tenant-01", "description": "Compute"}
        )
        assert create_res.status_code == 201
        item = create_res.json()
        assert item["title"] == "Cloud Server"
        assert item["tenant_id"] == "tenant-01"

        list_res = await client.get("/api/v1/items?tenant_id=tenant-01")
        assert list_res.status_code == 200
        items = list_res.json()
        assert len(items) >= 1

@pytest.mark.asyncio
async def test_tenant_isolation_get():
    async with AsyncTestClient(app=app) as client:
        create_res = await client.post(
            "/api/v1/items",
            json={"title": "Secret Record", "tenant_id": "tenant-corp-a"}
        )
        item_id = create_res.json()["id"]

        # Cross-tenant query must return 404 Not Found
        denied_res = await client.get(f"/api/v1/items/{item_id}?tenant_id=tenant-corp-b")
        assert denied_res.status_code == 404

        # Matching tenant query returns 200 OK
        allowed_res = await client.get(f"/api/v1/items/{item_id}?tenant_id=tenant-corp-a")
        assert allowed_res.status_code == 200
