# Quality scenarios

## Stakeholders

| Who | What they care about |
|---|---|
| Guest | Finds a free room quickly; never loses a booking |
| Receptionist | Never promises one room twice; can cancel at the desk |
| Hotel manager (domain expert) | Knows the rules; wants deposits and SMS soon |
| Development team | Can change one area without breaking the others |
| Email/SMS and payment providers | Outside systems that can be slow or down |

## S1 · Performance: many guests search at once

| Part | S1 |
|---|---|
| Source | 200 guests |
| Stimulus | They search free rooms for 12–14 Nov |
| Environment | Within one minute |
| Artifact | The free-room search in BookingService (find_free_rooms) |
| Response | Every guest gets the correct list of free rooms |
| Measure | p95 response time ≤ 1 second |
| Checked in | P08 (cache), P23 (load test) |

## S2 · Data integrity: no double booking

| Part | S2 |
|---|---|
| Source | 100 pairs of guests |
| Stimulus | Both guests of a pair book the same room and nights at the same moment |
| Environment | Normal operation, many bookings at once |
| Artifact | BookingService.reserve and the reservation store |
| Response | Exactly one Confirmed reservation per pair; the other guest is told the room is unavailable |
| Measure | 0 double bookings |
| Checked in | P09 |

## S3 · Availability: a failed message keeps the booking

| Part | S3 |
|---|---|
| Source | The email provider |
| Stimulus | It stops answering |
| Environment | For 10 minutes, during normal bookings |
| Artifact | BookingService.reserve and the notification sender |
| Response | Every valid booking is still Accepted and saved; the failed message is reported |
| Measure | 0 lost bookings; every failed message is counted |
| Checked in | P04 (R6 test, done) and P10 |

## S4 · Security: nobody reads another guest's reservation

| Part | S4 |
|---|---|
| Source | A guest (or an attacker) |
| Stimulus | Tries 100 times to read another guest's reservation |
| Environment | Normal operation, through the public API |
| Artifact | The reservation lookup and its access check |
| Response | Every attempt is refused; no data of the other guest is shown |
| Measure | 0 reservations shown to the wrong guest (out of 100 attempts) |
| Checked in | P21 |

## S5 · Modifiability: adding SMS confirmations

| Part | S5 |
|---|---|
| Source | The hotel (manager) |
| Stimulus | Asks for SMS confirmations as well as email |
| Environment | During development, before the next release |
| Artifact | The notification sender and BookingService |
| Response | A new sender class is added; BookingService is not edited |
| Measure | BookingService edited 0 times; at most 2 files change |
| Checked in | P04 (SMS sender, done) |

## S6 · Sustainability: less energy for the same work

| Part | S6 |
|---|---|
| Source | The development team |
| Stimulus | Makes a change (for example a cache for the free-room search) |
| Environment | The same 1,000 completed searches, before and after the change |
| Artifact | The free-room search on the server |
| Response | The same searches are answered with less energy |
| Measure | At least 20% fewer watt-hours per 1,000 completed searches |
| Checked in | P08, P24 |