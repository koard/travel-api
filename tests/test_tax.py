import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_calculate_tax(client: AsyncClient):
    # เพิ่ม province ที่จะใช้ทดสอบ
    await client.post("/v1/provinces/", json={
        "name": "Chiang Mai",
        "is_secondary": True
    })

    # คำนวณลดหย่อนภาษี
    payload = {
        "province_name": "Chiang Mai",
        "amount": 10000
    }
    response = await client.post("/v1/tax/calculate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["province"] == "Chiang Mai"
    assert data["amount"] == 10000
    assert data["is_secondary"] is True
    assert data["deductible"] == 2000.0  # 20% ของ 10000
