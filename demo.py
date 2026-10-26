from datetime import date

from hotel_booking.booking_service import BookingService
from hotel_booking.domain import DateRange, Guest, Room
from hotel_booking.notifications import EmailSender
from hotel_booking.store import InMemoryReservationStore


def nov(check_in_day, check_out_day):
    return DateRange(date(2026, 11, check_in_day), date(2026, 11, check_out_day))


maya = Guest("Maya", "maya@example.com")
omar = Guest("Omar", "omar@example.com")
r7 = Room("R7", "Standard")
r8 = Room("R8", "Deluxe")

service = BookingService([r7, r8], InMemoryReservationStore(), EmailSender())

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