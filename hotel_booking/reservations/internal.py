from __future__ import annotations
from typing import Optional
from hotel_booking.reservations.domain import Reservation


class InMemoryReservationStore:
    """Keeps reservations in a list. P07 adds a PostgreSQL store with the same methods."""

    def __init__(self) -> None:
        self._reservations: list[Reservation] = []

    def next_id(self) -> str:
        return f"R{101 + len(self._reservations)}"

    def add(self, reservation: Reservation) -> None:
        self._reservations.append(reservation)

    def get(self, reservation_id: str) -> Optional[Reservation]:
        for reservation in self._reservations:
            if reservation.id == reservation_id:
                return reservation
        return None

    def all(self) -> list[Reservation]:
        return list(self._reservations)

    def count(self) -> int:
        return len(self._reservations)