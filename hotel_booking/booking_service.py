from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from hotel_booking.domain import (
    DateRange, Guest, Reservation, ReservationStatus, Room,
)
from hotel_booking.notifications import NotificationSender
from hotel_booking.store import ReservationStore


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
    def __init__(self, rooms: list[Room], store: ReservationStore,
                 sender: NotificationSender) -> None:
        self._rooms = rooms
        self._store = store
        self._sender = sender

    def reserve(self, guest: Guest, room: Room, stay: DateRange) -> BookingResult:
        if not stay.is_valid():
            return BookingResult(False, reason="Invalid dates")

        if any(r.blocks(room, stay) for r in self._store.all()):
            return BookingResult(False, reason="Unavailable")

        reservation = Reservation(
            self._store.next_id(), guest, room, stay, ReservationStatus.CONFIRMED
        )
        self._store.add(reservation)

        # R6: xabar yuborilmasa ham bron saqlanib qoladi.
        notification_failed = False
        try:
            self._sender.send_confirmation(reservation)
        except Exception:
            notification_failed = True

        return BookingResult(True, reservation.id, notification_failed=notification_failed)

    def cancel(self, reservation_id: str) -> bool:
        reservation = self._store.get(reservation_id)
        if reservation is None:
            return False
        reservation.status = ReservationStatus.CANCELLED
        return True

    def find_free_rooms(self, stay: DateRange) -> list[Room]:
        return [
            room for room in self._rooms
            if not any(r.blocks(room, stay) for r in self._store.all())
        ]