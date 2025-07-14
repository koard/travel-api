import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_province(client: AsyncClient):
    payload = {
        "name": "Chiang Mai",
        "is_secondary": False
    }
    response = await client.post("/v1/provinces/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["is_secondary"] == payload["is_secondary"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_all_provinces(client: AsyncClient):
    # ต้องสร้าง province ไว้ก่อน
    await client.post("/v1/provinces/", json={
        "name": "Test City",
        "is_secondary": False
    })

    # ค่อย GET
    response = await client.get("/v1/provinces/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_province_by_id(client: AsyncClient):
    # สร้างก่อน
    create_resp = await client.post("/v1/provinces/", json={
        "name": "Rayong",
        "is_secondary": True
    })
    assert create_resp.status_code == 201
    province_id = create_resp.json()["id"]

    # ดึงจาก ID
    response = await client.get(f"/v1/provinces/{province_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Rayong"
    assert data["is_secondary"] is True

@pytest.mark.asyncio
async def test_update_province(client: AsyncClient):
    create_resp = await client.post("/v1/provinces/", json={
        "name": "Lampang",
        "is_secondary": True
    })
    province_id = create_resp.json()["id"]

    updated_data = {
        "name": "Lampang Updated",
        "is_secondary": False
    }
    response = await client.put(f"/v1/provinces/{province_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Lampang Updated"
    assert data["is_secondary"] is False

@pytest.mark.asyncio
async def test_delete_province(client: AsyncClient):
    create_resp = await client.post("/v1/provinces/", json={
        "name": "Nan",
        "is_secondary": True
    })
    province_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/v1/provinces/{province_id}")
    assert delete_resp.status_code == 204

    # เช็คว่าไม่มีแล้ว
    get_resp = await client.get(f"/v1/provinces/{province_id}")
    assert get_resp.status_code == 404
