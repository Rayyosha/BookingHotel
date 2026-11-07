# P03 design notes

## Why design before code

Low-level design kod yozishdan oldin qaysi sinflar (masalan, Guest, Room,
Reservation) bo'lishini, har bir sinf qanday ma'lumot saqlashini va qanday
metodlarga ega bo'lishini, hamda qaysi sinf qaysi sinfni chaqirishini hal qiladi.

# P04 design notes

## Refactoring
Refactoring changes how the code is organised, but not what the app does for the guest.

Must stay the same:
- The tests: all of them still pass after every move.
- The demo output: the same lines as in P03.
- The race demo: still shows "Double booking!" (refactoring does not fix bugs).

## What our code breaks
- BookingService asked for exactly ReservationStore (D: dependency inversion).
  In P07 we would have to edit BookingService just to use a database.
- BookingService asked for exactly EmailSender (D and O). Adding SMS would mean
  editing BookingService.

## Proof
- Tests: 8 passing
- Demo: same output as before the refactoring
- Race: still double-books (fixed later, in P09)




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

# P07 design notes
## API decisions
- Free rooms come in text order of the room number (R10 comes before R7), and "after" compares text too.
- Clients compare the error "title"; "detail" is a sentence for people and may change.
- The room type is catalog data from the rooms table, not a fixed list.
- ## Docker
Port 5432 was taken on my Mac, so docker-compose.yml publishes PostgreSQL on 15432.

## API tests
- Search: GET /rooms/availability -> 200 with R7 and R8
- Book twice: POST Maya -> 201 R101, POST Omar -> 409 Unavailable
- Wrong dates: POST with checkOut = checkIn -> 400 InvalidDates (problem+json)
- Cancel twice: DELETE R101 -> 204, then 404 NotFound


## After
- Checks: 12 tests green (8 booking + 4 API), 3 import-linter contracts kept
- Seven API answers match the contract (docs/api-check.md)
- Restart check: the booking survives a restart, it lives in PostgreSQL

# P08 design notes

## Cache rule
Booking never reads the cache: BookingService always asks PostgreSQL.

## Cache decisions
- Key availability:v{version}:{checkIn}:{checkOut}, TTL 30 s, only the free-room search is cached.
- A successful POST (201) and DELETE (204) raise availability:version, after the unit of work has saved.
- Redis port 6379 (HOTEL_REDIS_PORT if taken); PostgreSQL stays on 15432.

## After
- Checks: 14 tests green (8 booking + 6 API), 3 import-linter contracts kept
- Measurements: no cache vs cache-aside (see docs/cache-experiment.md)
- Stale result: seen without invalidation, fixed with the version number
