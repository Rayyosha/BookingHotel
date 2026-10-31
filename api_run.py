from contextlib import contextmanager

import uvicorn

from hotel_booking.api import create_app
from hotel_booking.notifications.internal import EmailSender
from hotel_booking.reservations import BookingService
from hotel_booking.reservations.internal import InMemoryReservationStore
from hotel_booking.rooms import Room

rooms = [Room("R7", "Standard"), Room("R8", "Deluxe")]
service = BookingService(rooms, InMemoryReservationStore(), EmailSender())


@contextmanager
def unit_of_work():
    yield service


uvicorn.run(create_app(rooms, unit_of_work), host="localhost", port=5080)