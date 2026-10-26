from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


@dataclass(frozen=True)
class Guest:
    name: str
    email: str


@dataclass(frozen=True)
class Room:
    number: str
    type: str


@dataclass(frozen=True)
class DateRange:
    check_in: date
    check_out: date

    def is_valid(self) -> bool:
        return self.check_out > self.check_in

    # Ikki turar joy kamida bitta umumiy tunga ega bo'lsa, ular kesishadi.
    # 12-14 va 14-16 noyabr kesishmaydi (14-kuni birinchi mehmon ketadi).
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

    # Faqat Confirmed bron xonani to'sadi. Cancelled bron to'smaydi.
    def blocks(self, room: Room, stay: DateRange) -> bool:
        return (
            self.status == ReservationStatus.CONFIRMED
            and self.room == room
            and self.stay.overlaps(stay)
        )