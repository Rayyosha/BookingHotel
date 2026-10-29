from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Room:
    number: str
    type: str


class RoomCatalog(Protocol):
    """Rooms' public contract: which rooms the hotel sells."""

    def all(self) -> list[Room]: ...