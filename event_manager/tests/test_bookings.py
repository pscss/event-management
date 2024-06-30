from datetime import datetime

import pytest
import pytz
from faker import Faker
from httpx import AsyncClient

base_route = "http://127.0.0.1:8080/bookings/"

faker = Faker()


async def create_user(client: AsyncClient):
    user_data = user_data = {
        "name": faker.name(),
        "email": faker.email(),
        "country_code": faker.country_code(),
        "phone_number": faker.numerify("##########"),
    }

    response = await client.post("http://127.0.0.1:8080/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    return int(data["id"])


async def create_event(client: AsyncClient):
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

    response = await client.post("http://127.0.0.1:8080/events/", json=event_data)
    assert response.status_code == 200
    data = response.json()
    return int(data["id"]), event_data["base_price"]


@pytest.mark.asyncio
async def test_create_booking(client: AsyncClient):
    user_id = await create_user(client)
    event_id, base_price = await create_event(client)
    booking_data = {
        "event_id": user_id,
        "user_id": event_id,
        "booking_time": datetime(2024, 8, 15, 14, 0, 0, tzinfo=pytz.UTC).isoformat(),
        "quantity": faker.random_digit_above_two(),
    }

    response = await client.post(base_route, json=booking_data)
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == booking_data["event_id"]
    assert data["user_id"] == booking_data["user_id"]
    assert data["booking_time"]
    assert data["quantity"] == booking_data["quantity"]
    assert data["total_cost"] == base_price * booking_data["quantity"]
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_get_all_bookings(client: AsyncClient):
    user_id = await create_user(client)
    event_id, _ = await create_event(client)
    booking_data = {
        "event_id": user_id,
        "user_id": event_id,
        "booking_time": datetime(2024, 8, 15, 14, 0, 0, tzinfo=pytz.UTC).isoformat(),
        "quantity": faker.random_digit_above_two(),
    }

    response = await client.post(base_route, json=booking_data)
    assert response.status_code == 200
    data = response.json()

    response = await client.get(base_route)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_delete_booking(client: AsyncClient):
    user_id = await create_user(client)
    event_id, _ = await create_event(client)
    booking_data = {
        "event_id": user_id,
        "user_id": event_id,
        "booking_time": datetime(2024, 8, 15, 14, 0, 0, tzinfo=pytz.UTC).isoformat(),
        "quantity": faker.random_digit_above_two(),
    }

    response = await client.post(base_route, json=booking_data)
    assert response.status_code == 200
    data = response.json()
    booking_id = data["id"]
    response = await client.delete(f"{base_route}{booking_id}")
    assert response.status_code == 200
