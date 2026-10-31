from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional, Protocol

from hotel_booking.notifications import Confirmation, NotificationSender
from hotel_booking.reservations.domain import (
    DateRange, Guest, Reservation, ReservationStatus,
)
from hotel_booking.rooms import Room


class ReservationStore(Protocol):
    """What BookingService needs from storage. Today a list in memory; from P07 a database."""

    def next_id(self) -> str: ...
    def add(self, reservation: Reservation) -> None: ...
    def get(self, reservation_id: str) -> Optional[Reservation]: ...
    def all(self) -> list[Reservation]: ...
    def count(self) -> int: ...


@dataclass
class BookingResult:
    accepted: bool
    reservation_id: Optional[str] = None
    reason: str = ""
    notification_failed: bool = False

    def __str__(self) -> str:
        if self.accepted:
            return f"Accepted {self.reservation_id}"
        return self.reason


class BookingService:
    """Owns the booking rule. Uses only the public contracts of Rooms and Notifications."""

    def __init__(self, rooms: list[Room], store: ReservationStore,
                 sender: NotificationSender, slow_step_seconds: float = 0) -> None:
        self._rooms = rooms
        self._store = store
        self._sender = sender
        self._slow_step_seconds = slow_step_seconds

    def reserve(self, guest: Guest, room: Room, stay: DateRange) -> BookingResult:
        if not stay.is_valid():
            return BookingResult(False, reason="Invalid dates")

        if any(r.blocks(room, stay) for r in self._store.all()):
            return BookingResult(False, reason="Unavailable")

        time.sleep(self._slow_step_seconds)  # 0 normally; the race demo makes this step slow

        reservation = Reservation(
            self._store.next_id(), guest, room, stay, ReservationStatus.CONFIRMED
        )
        self._store.add(reservation)

        # R6: xabar yuborilmasa ham bron saqlanib qoladi.
        notification_failed = False
        try:
            # Notifications gets its own message: the five fields it needs, not the Reservation.
            self._sender.send_confirmation(
                Confirmation(reservation.id, guest.email, room.number,
                             stay.check_in, stay.check_out))
        except Exception:
            notification_failed = True

        return BookingResult(True, reservation.id, notification_failed=notification_failed)

    def cancel(self, reservation_id: str) -> bool:
        reservation = self._store.get(reservation_id)
        if reservation is None or reservation.status == ReservationStatus.CANCELLED:
            return False
        reservation.status = ReservationStatus.CANCELLED
        return True

    def find_free_rooms(self, stay: DateRange) -> list[Room]:
        return [
            room for room in self._rooms
            if not any(r.blocks(room, stay) for r in self._store.all())
        ]