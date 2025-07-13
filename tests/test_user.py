import pytest


@pytest.fixture
def user_data():
    return {
        "full_name": "Alice Test",
        "citizen_id": "1234567890123",
        "phone": "0812345678",
        "province_id": 1,
        "email": "alice@example.com",
        "password": "password"
    }


@pytest.mark.asyncio
async def test_create_user(client, user_data):
    resp = await client.post("/v1/users/", json=user_data)
    assert resp.status_code == 201
    data = resp.json()
    assert data["full_name"] == user_data["full_name"]
    assert data["email"] == user_data["email"]
    assert "id" in data


@pytest.mark.asyncio
async def test_get_all_users(client):
    resp = await client.get("/v1/users/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_get_user_by_id(client, user_data):
    create_resp = await client.post("/v1/users/", json=user_data)
    user_id = create_resp.json()["id"]

    resp = await client.get(f"/v1/users/{user_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == user_id


@pytest.mark.asyncio
async def test_update_user(client, user_data):
    create_resp = await client.post("/v1/users/", json=user_data)
    user_id = create_resp.json()["id"]

    updated_data = user_data.copy()
    updated_data["full_name"] = "Updated Name"

    resp = await client.put(f"/v1/users/{user_id}", json=updated_data)
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_user(client, user_data):
    create_resp = await client.post("/v1/users/", json=user_data)
    user_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/v1/users/{user_id}")
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/v1/users/{user_id}")
    assert get_resp.status_code == 404
