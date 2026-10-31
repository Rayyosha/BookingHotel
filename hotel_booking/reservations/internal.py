from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from hotel_booking.reservations.domain import DateRange, Guest, Reservation, ReservationStatus
from hotel_booking.rooms import Room


class InMemoryReservationStore:
    """Keeps reservations in a list. PostgresReservationStore below has the same methods."""

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


class ReservationsTables(DeclarativeBase):
    """The tables the Reservations module owns."""


class ReservationRow(ReservationsTables):
    """One row of the reservations table in db/init.sql."""
    __tablename__ = "reservations"
    id: Mapped[str] = mapped_column(primary_key=True)
    guest_name: Mapped[str]
    guest_email: Mapped[str]
    room: Mapped[str]
    check_in: Mapped[date]
    check_out: Mapped[date]
    status: Mapped[str]


class PostgresReservationStore:
    """Keeps reservations in PostgreSQL. One store per request (a unit of work): it remembers the
    reservations it hands out, and save_changes writes their changed status and commits."""

    def __init__(self, session: Session, rooms: list[Room]) -> None:
        self._session = session
        self._rooms = {room.number: room for room in rooms}
        self._loaded: list[tuple[ReservationRow, Reservation]] = []

    def _to_domain(self, row: ReservationRow) -> Reservation:
        status = ReservationStatus.CANCELLED if row.status == "Cancelled" else ReservationStatus.CONFIRMED
        reservation = Reservation(row.id, Guest(row.guest_name, row.guest_email), self._rooms[row.room],
                                  DateRange(row.check_in, row.check_out), status)
        self._loaded.append((row, reservation))
        return reservation

    def next_id(self) -> str:
        return f"R{101 + self.count()}"

    def add(self, reservation: Reservation) -> None:
        self._session.add(ReservationRow(
            id=reservation.id, guest_name=reservation.guest.name, guest_email=reservation.guest.email,
            room=reservation.room.number, check_in=reservation.stay.check_in,
            check_out=reservation.stay.check_out, status=reservation.status.value))
        self._session.flush()  # INSERT now: a second R101 is refused here

    def get(self, reservation_id: str) -> Optional[Reservation]:
        row = self._session.get(ReservationRow, reservation_id)
        return None if row is None else self._to_domain(row)

    def all(self) -> list[Reservation]:
        return [self._to_domain(row) for row in self._session.scalars(select(ReservationRow))]

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(ReservationRow))

    def save_changes(self) -> None:
        """End of the request: copy each loaded reservation's status to its row and commit."""
        for row, reservation in self._loaded:
            row.status = reservation.status.value
        self._session.commit()