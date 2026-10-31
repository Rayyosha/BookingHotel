import os
from contextlib import contextmanager

import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from hotel_booking.api import create_app
from hotel_booking.notifications.internal import EmailSender
from hotel_booking.reservations import BookingService
from hotel_booking.reservations.internal import PostgresReservationStore
from hotel_booking.rooms.internal import PostgresRoomCatalog

# The wiring: PostgreSQL from docker-compose.yml (port 15432 on this laptop).
engine = create_engine(f"postgresql+psycopg://hotel:hotel@localhost:{os.getenv('HOTEL_DB_PORT', '15432')}/hotel")
rooms = PostgresRoomCatalog(engine).all()
email = EmailSender()


@contextmanager
def unit_of_work():
    # One request: a fresh store over its own session; save what changed at the end.
    with Session(engine) as session:
        store = PostgresReservationStore(session, rooms)
        yield BookingService(rooms, store, email)
        store.save_changes()


uvicorn.run(create_app(rooms, unit_of_work), host="localhost", port=5080)