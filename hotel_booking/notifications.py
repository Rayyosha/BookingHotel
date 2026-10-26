from __future__ import annotations

from typing import Protocol

from hotel_booking.domain import Reservation


class NotificationSender(Protocol):
    def send_confirmation(self, reservation: Reservation) -> None: ...


class EmailSender:
    def send_confirmation(self, reservation: Reservation) -> None:
        print(f"  [email -> {reservation.guest.email}] {reservation.id} tasdiqlandi: "
              f"xona {reservation.room.number}")


class SmsSender:
    def send_confirmation(self, reservation: Reservation) -> None:
        print(f"  [sms -> {reservation.guest.name}] {reservation.id} tasdiqlandi: "
              f"xona {reservation.room.number}")