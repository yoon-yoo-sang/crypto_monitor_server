import os

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from app.main import app


load_dotenv()


admin_token = os.getenv("ADMIN_TOKEN")
header = {"Authorization": f"Bearer {admin_token}"}


@pytest.mark.asyncio
async def test_get_coin_details():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/coins/100", headers=header)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 100
    assert "market" in data


@pytest.mark.asyncio
async def test_get_coin_histories():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/coins/1/histories", headers=header)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert "price" in data[0]
        assert "timestamp" in data[0]
