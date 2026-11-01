# API check: seven requests against PostgreSQL

1. Search 12-14 Nov: 200, R7 and R8 free ✓
2. Maya books R7 12-14 Nov: 201 R101 ✓
3. Omar books R7 13-15 Nov: 409 Unavailable ✓
4. Omar books R8 15-15 Nov: 400 InvalidDates ✓
5. Search 12-14 Nov again: 200, only R8 free ✓
6. Cancel R101: 204 ✓
7. Cancel R101 again: 404 NotFound ✓

## Restart check
Booked Maya again (201 R102), stopped and restarted the app, searched 12-14 Nov: only R8 is free ✓

## Reservations table
R101 Maya R7 Cancelled
R102 Maya R7 Confirmed