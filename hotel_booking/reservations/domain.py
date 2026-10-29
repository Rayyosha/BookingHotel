from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from enum import Enum
from hotel_booking.rooms import Room


@dataclass(frozen=True)
class Guest:
    name: str
    email: str


@dataclass(frozen=True)
class DateRange:
    check_in: date
    check_out: date

    def is_valid(self) -> bool:
        return self.check_out > self.check_in

    def overlaps(self, other: DateRange) -> bool:
        return self.check_in < other.check_out and other.check_in < self.check_out


class ReservationStatus(Enum):
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"


@dataclass
class Reservation:
    id: str
    guest: Guest
    room: Room
    stay: DateRange
    status: ReservationStatus

    def blocks(self, room: Room, stay: DateRange) -> bool:
        return (
            self.status == ReservationStatus.CONFIRMED
            and self.room == room
            and self.stay.overlaps(stay)
        )