from __future__ import annotations

from hotel_booking.notifications import Confirmation


class EmailSender:
    def send_confirmation(self, confirmation: Confirmation) -> None:
        print(f"  [email -> {confirmation.guest_email}] {confirmation.reservation_id} tasdiqlandi: "
              f"xona {confirmation.room_number}")


class SmsSender:
    def send_confirmation(self, confirmation: Confirmation) -> None:
        print(f"  [sms -> {confirmation.guest_email}] {confirmation.reservation_id} tasdiqlandi: "
              f"xona {confirmation.room_number}")