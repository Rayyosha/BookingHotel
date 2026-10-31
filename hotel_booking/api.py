"""The HTTP API: three endpoints that turn HTTP requests into BookingService calls and back.

It lives outside the four modules and uses only their public contracts.
"""
from __future__ import annotations

from contextlib import AbstractContextManager
from pathlib import Path
from typing import Callable

from fastapi import FastAPI
from fastapi.responses import Response

from hotel_booking.reservations import BookingService
from hotel_booking.rooms import Room

# One request's work: "with unit_of_work() as service:" gives the endpoint a BookingService.
UnitOfWork = Callable[[], AbstractContextManager[BookingService]]

CONTRACT = Path("docs") / "openapi.yaml"


def create_app(rooms: list[Room], unit_of_work: UnitOfWork) -> FastAPI:
    # docs/openapi.yaml is the contract, so FastAPI must not publish one of its own.
    app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)

    @app.get("/openapi.yaml")
    def contract() -> Response:
        path = CONTRACT if CONTRACT.exists() else Path(__file__).resolve().parent.parent / "docs" / "openapi.yaml"
        return Response(path.read_text(encoding="utf-8"), media_type="application/yaml")

    return app