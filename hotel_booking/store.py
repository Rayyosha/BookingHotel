from __future__ import annotations

from typing import Optional, Protocol

from hotel_booking.domain import Reservation


class ReservationStore(Protocol):
    def next_id(self) -> str: ...
    def add(self, reservation: Reservation) -> None: ...
    def get(self, reservation_id: str) -> Optional[Reservation]: ...
    def all(self) -> list[Reservation]: ...
    def count(self) -> int: ...


class InMemoryReservationStore:
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