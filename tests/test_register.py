import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client):
    payload = {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "secret123"
    }

    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "secret123"
    }

    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert "Email already registered" in response.text
