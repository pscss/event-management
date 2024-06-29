"""Add seed data

Revision ID: ad09d94ffe59
Revises: e913e1718f21
Create Date: 2024-06-29 15:19:19.072052

"""

from datetime import datetime

import pytz
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "ad09d94ffe59"
down_revision = "e913e1718f21"
branch_labels = None
depends_on = None


def upgrade() -> None:
    meta = sa.MetaData()
    bind = op.get_bind()

    # """ pass in tuple with tables we want to reflect,
    # otherwise whole database will get reflected"""
    meta.reflect(
        bind=bind,
        only=(
            "users",
            "events",
        ),
    )

    # define table representation
    user = sa.Table("users", meta)
    event = sa.Table("events", meta)
    # Insert seed data into the users table
    op.bulk_insert(
        user,
        [
            {
                "name": "Alice",
                "email": "alice@example.com",
                "country_code": "+91",
                "phone_number": "1234567890",
            },
            {
                "name": "Bob",
                "email": "bob@example.com",
                "country_code": "+91",
                "phone_number": "0987654321",
            },
        ],
    )

    # Insert seed data into the events table
    op.bulk_insert(
        event,
        [
            {
                "name": "Conference",
                "event_date": datetime(2024, 7, 10).date(),
                "event_time": datetime(2024, 7, 10, 10, 0, tzinfo=pytz.UTC),
                "venue": "Convention Center",
                "location_lat": 12.9715987,
                "location_long": 77.594566,
                "available_tickets": 100,
                "base_price": 50.0,
            },
            {
                "name": "Workshop",
                "event_date": datetime(2024, 8, 15).date(),
                "event_time": datetime(2024, 8, 15, 14, 0, tzinfo=pytz.UTC),
                "venue": "Tech Hub",
                "location_lat": 12.935242,
                "location_long": 77.624847,
                "available_tickets": 50,
                "base_price": 75.0,
            },
        ],
    )


def downgrade() -> None:
    pass
