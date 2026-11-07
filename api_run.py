import os
from contextlib import contextmanager

import uvicorn
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from hotel_booking.api import CountingReservationStore, Stats, create_app
from hotel_booking.api_cache import AvailabilityCache, RedisKeyValueStore
from hotel_booking.notifications.internal import EmailSender
from hotel_booking.reservations import BookingService
from hotel_booking.reservations.internal import PostgresReservationStore
from hotel_booking.rooms.internal import PostgresRoomCatalog


# The wiring: PostgreSQL (port 15432 on this laptop) and Redis (port 6379) from docker-compose.yml.
engine = create_engine(f"postgresql+psycopg://hotel:hotel@localhost:{os.getenv('HOTEL_DB_PORT', '15432')}/hotel")
rooms = PostgresRoomCatalog(engine).all()
email = EmailSender()
stats = Stats()
redis = Redis(host="localhost", port=int(os.getenv("HOTEL_REDIS_PORT", "6379")), decode_responses=True)
redis.ping()  # stop here if Redis is not running
cache = AvailabilityCache(RedisKeyValueStore(redis))


@contextmanager
def unit_of_work():
    # One request: a fresh store over its own session, counted for GET /stats; save what changed at the end.
    with Session(engine) as session:
        store = PostgresReservationStore(session, rooms)
        yield BookingService(rooms, CountingReservationStore(store, stats), email)
        store.save_changes()


uvicorn.run(create_app(rooms, unit_of_work, stats, cache), host="localhost", port=5080)