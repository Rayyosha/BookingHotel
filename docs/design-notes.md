# P03 design notes

## Why design before code

Low-level design kod yozishdan oldin qaysi sinflar (masalan, Guest, Room,
Reservation) bo'lishini, har bir sinf qanday ma'lumot saqlashini va qanday
metodlarga ega bo'lishini, hamda qaysi sinf qaysi sinfni chaqirishini hal qiladi.


# P06 design notes

## Before
- Tests: 8 passing
- Demo: the nine lines match the expected output
- Race: still double-books (Double booking!)

## Architecture rules
1. Reservations uses only the public contracts of other modules (never their internal code).
2. Rooms does not depend on any other module.
3. Payments and Notifications never depend on Reservations.

## Broken on purpose
Rule 1 failed ("Reservations uses only the public contracts of other modules").
The message named hotel_booking.reservations.booking -> hotel_booking.notifications.internal (l.11).
I removed the line and all checks were green again.

## After
- Tests: 8 passing, 3 import-linter contracts kept
- Demo: same output as Before
- Race: not added (demo.py has no --race)

- Race: python demo.py --race still double-books (Double booking!)