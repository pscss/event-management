import pytest
from faker import Faker
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

base_route = "http://127.0.0.1:8080/events/"

faker = Faker()


@pytest.mark.asyncio
async def test_create_event(client: AsyncClient):
    event_data = {
        "name": "WorkShop",
        "event_date": "2024-06-30",
        "event_time": "11:15:05.547Z",
        "venue": faker.address(),
        "location_lat": -89,
        "location_long": -179,
        "available_tickets": 10,
        "base_price": 100,
    }

    response = await client.post(base_route, json=event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == event_data["name"]
    assert data["venue"] == event_data["venue"]
    assert data["event_date"] == event_data["event_date"]
    assert data["available_tickets"] == event_data["available_tickets"]
    assert data["location_lat"] == event_data["location_lat"]
    assert data["location_long"] == event_data["location_long"]
    assert data["base_price"] == event_data["base_price"]
    assert data["id"]


@pytest.mark.asyncio
async def test_get_all_events(client: AsyncClient):
    event_data = {
        "name": faker.name(),
        "event_date": "2024-06-30",
        "event_time": "11:15:05.547Z",
        "venue": faker.address(),
        "location_lat": -89,
        "location_long": -179,
        "available_tickets": 10,
        "base_price": 100,
    }

    response = await client.post(base_route, json=event_data)
    assert response.status_code == 200

    response = await client.get(base_route)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_update_event(client: AsyncClient, session: AsyncSession):
    event_data = {
        "name": faker.name(),
        "event_date": "2024-06-30",
        "event_time": "11:15:05.547Z",
        "venue": faker.address(),
        "location_lat": -89,
        "location_long": -179,
        "available_tickets": 10,
        "base_price": 100,
    }

    response = await client.post(base_route, json=event_data)
    assert response.status_code == 200
    data = response.json()
    event_id = data["id"]

    update_event_data = {
        "name": "Updated Event",
        "event_date": "2024-07-02",
        "venue": "Bengaluru",
        "base_price": 150,
        "available_tickets": 30,
    }

    response = await client.put(f"{base_route}{event_id}", json=update_event_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_event_data["name"]
    assert data["event_date"] == update_event_data["event_date"]
    assert data["venue"] == update_event_data["venue"]
    assert data["base_price"] == update_event_data["base_price"]
    assert data["available_tickets"] == update_event_data["available_tickets"]


@pytest.mark.asyncio
async def test_delete_event(client: AsyncClient):
    event_data = {
        "name": faker.name(),
        "event_date": "2024-06-30",
        "event_time": "11:15:05.547Z",
        "venue": faker.address(),
        "location_lat": -89,
        "location_long": -179,
        "available_tickets": 10,
        "base_price": 100,
    }

    response = await client.post(base_route, json=event_data)
    assert response.status_code == 200
    data = response.json()
    event_id = data["id"]
    response = await client.delete(f"{base_route}{event_id}")
    assert response.status_code == 200
