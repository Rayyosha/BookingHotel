import sys
import threading
import time
from datetime import date

from hotel_booking.notifications.internal import EmailSender
from hotel_booking.reservations import BookingService, DateRange, Guest
from hotel_booking.reservations.internal import InMemoryReservationStore
from hotel_booking.rooms import Room
from hotel_booking.rooms.internal import InMemoryRoomCatalog


def nov(check_in_day, check_out_day):
    return DateRange(date(2026, 11, check_in_day), date(2026, 11, check_out_day))


maya = Guest("Maya", "maya@example.com")
omar = Guest("Omar", "omar@example.com")
r7 = Room("R7", "Standard")
r8 = Room("R8", "Deluxe")

# The wiring: the only app code that names the internal classes of the modules.
catalog = InMemoryRoomCatalog([r7, r8])


def run_demo():
    service = BookingService(catalog.all(), InMemoryReservationStore(), EmailSender())

    print("1. Maya R7 ni 12-14 noyabrga bron qiladi:")
    print("2. ", service.reserve(maya, r7, nov(12, 14)))
    print("3. Omar R7 ni 13-15 noyabrga bron qiladi:")
    print("4. ", service.reserve(omar, r7, nov(13, 15)))
    print("5. Omar R7 ni 14-16 noyabrga bron qiladi:")
    print("6. ", service.reserve(omar, r7, nov(14, 16)))
    print("7. Maya R101 ni bekor qiladi:", service.cancel("R101"))
    print("8. 12-14 noyabrda bo'sh xonalar:",
          [room.number for room in service.find_free_rooms(nov(12, 14))])
    print("9. Tayyor.")


def run_race():
    store = InMemoryReservationStore()
    # Each request now spends half a second between checking and saving.
    service = BookingService(catalog.all(), store, EmailSender(), slow_step_seconds=0.5)
    stay = nov(12, 14)
    results = {}

    print("Maya and Omar both book R7 for 12-14 Nov at the same moment...")
    maya_request = threading.Thread(target=lambda: results.update(Maya=service.reserve(maya, r7, stay)))
    omar_request = threading.Thread(target=lambda: results.update(Omar=service.reserve(omar, r7, stay)))
    maya_request.start()
    time.sleep(0.1)  # Omar clicks a moment after Maya
    omar_request.start()
    maya_request.join()
    omar_request.join()

    print(f"Maya: {results['Maya']}")
    print(f"Omar: {results['Omar']}")
    confirmed = sum(1 for r in store.all() if r.blocks(r7, stay))
    print(f"Confirmed reservations for R7 on 12-14 Nov: {confirmed}")
    print("Double booking! Both requests checked before either one saved."
          if confirmed > 1 else "Only one guest has R7.")


if __name__ == "__main__":
    run_race() if "--race" in sys.argv else run_race()