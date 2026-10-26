import unittest
from datetime import date

from hotel_booking.booking_service import BookingService
from hotel_booking.domain import DateRange, Guest, Room
from hotel_booking.store import InMemoryReservationStore

MAYA = Guest("Maya", "maya@example.com")
OMAR = Guest("Omar", "omar@example.com")
R7 = Room("R7", "Standard")
R8 = Room("R8", "Deluxe")


def nov(check_in_day: int, check_out_day: int) -> DateRange:
    return DateRange(date(2026, 11, check_in_day), date(2026, 11, check_out_day))


class FakeSender:
    def __init__(self) -> None:
        self.sent = []

    def send_confirmation(self, reservation) -> None:
        self.sent.append(reservation)


class FailingSender:
    def send_confirmation(self, reservation) -> None:
        raise RuntimeError("email provider is down")


def new_service(failing_sender: bool = False):
    store = InMemoryReservationStore()
    sender = FailingSender() if failing_sender else FakeSender()
    service = BookingService([R7, R8], store, sender)
    return service, store, sender


class BookingTests(unittest.TestCase):
    def test_booking_a_free_room_is_accepted(self):
        service, store, _ = new_service()
        result = service.reserve(MAYA, R7, nov(12, 14))
        self.assertEqual("Accepted R101", str(result))
        self.assertEqual(1, store.count())

    def test_the_same_room_on_overlapping_nights_is_unavailable(self):
        service, store, _ = new_service()
        service.reserve(MAYA, R7, nov(12, 14))
        result = service.reserve(OMAR, R7, nov(13, 15))
        self.assertEqual("Unavailable", str(result))
        self.assertEqual(1, store.count())

    def test_back_to_back_stays_do_not_overlap(self):
        service, _, _ = new_service()
        service.reserve(MAYA, R7, nov(12, 14))
        result = service.reserve(OMAR, R7, nov(14, 16))
        self.assertEqual("Accepted R102", str(result))

    def test_check_out_must_be_after_check_in(self):
        service, store, _ = new_service()
        result = service.reserve(MAYA, R7, nov(14, 12))
        self.assertEqual("Invalid dates", str(result))
        self.assertEqual(0, store.count())

    def test_cancelling_frees_the_nights(self):
        service, _, _ = new_service()
        service.reserve(MAYA, R7, nov(12, 14))
        self.assertTrue(service.cancel("R101"))
        result = service.reserve(OMAR, R7, nov(12, 14))
        self.assertEqual("Accepted R102", str(result))

    def test_free_rooms_do_not_include_a_booked_room(self):
        service, _, _ = new_service()
        service.reserve(MAYA, R7, nov(12, 14))
        self.assertEqual([R8], service.find_free_rooms(nov(12, 14)))

    def test_a_confirmation_is_sent_after_booking(self):
        service, _, sender = new_service()
        service.reserve(MAYA, R7, nov(12, 14))
        self.assertEqual(1, len(sender.sent))
        self.assertEqual("R101", sender.sent[0].id)

    def test_a_failed_confirmation_keeps_the_booking(self):
        service, store, _ = new_service(failing_sender=True)
        result = service.reserve(MAYA, R7, nov(12, 14))
        self.assertEqual("Accepted R101", str(result))
        self.assertTrue(result.notification_failed)
        self.assertEqual(1, store.count())


if __name__ == "__main__":
    unittest.main()
