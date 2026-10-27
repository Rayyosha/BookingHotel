# Hotel contexts

## Words

| Word | Meaning here | Name in our code |
|---|---|---|
| Guest | A person who books a room; has a name and an email address | Guest |
| Room | One physical hotel room, such as R7 (Standard) or R8 (Deluxe) | Room (number, type) |
| Room type | The category of a room: Standard or Deluxe | Room.type |
| Nightly price | What one night in a room costs; Deluxe costs more than Standard | not in code yet |
| Out of service | A room that is closed for repairs and is not offered to guests | not in code yet |
| Stay | Check-in to check-out, half-open: 12–14 Nov = the nights of the 12th and 13th | DateRange (check_in, check_out) |
| Reservation | Guest + room + stay + status, with an id such as R101 | Reservation (id, guest, room, stay, status) |
| Confirmed | The room is promised to this guest for these nights | ReservationStatus.CONFIRMED |
| Cancelled | The promise is withdrawn; the nights are free again | ReservationStatus.CANCELLED |
| Book | A guest asks for a room for a stay; the answer is Accepted or Unavailable | BookingService.reserve(guest, room, stay) |
| Cancel | Withdraw a reservation, for example at the desk | BookingService.cancel(reservation_id) |
| Free rooms | The rooms with no Confirmed reservation that shares a night with the stay | BookingService.find_free_rooms(stay) |
| Deposit | 30% of the stay's price, taken when the guest books | not in code yet |
| Paid | The deposit was taken successfully | not in code yet |
| Declined | The deposit was refused (for example the card was declined) | not in code yet |
| Confirmation message | The email or SMS that tells the guest "R101 is confirmed: room R7, 12–14 Nov" | NotificationSender.send_confirmation(reservation) |
| Sent | The message arrived at the guest's provider | not in code yet |
| Failed | The message could not be sent; it is recorded and reported | not in code yet |

## Rooms

Job: knows which rooms the hotel sells.

| Word | Meaning here |
|---|---|
| Room | One physical hotel room, such as R7 (Standard) or R8 (Deluxe) |
| Room type | The category of a room: Standard or Deluxe |
| Nightly price | What one night in a room costs; depends on the room type |
| Out of service | A room that is closed for repairs and is not offered to guests |

Rules this context owns:
- A room that is out of service is not offered to guests.
- The nightly price depends on the room type (Deluxe costs more than Standard).

Needs from other contexts: nothing.
Tells other contexts: the list of rooms, when Reservations asks (answer to "which rooms exist?").

## Reservations

Job: decides whether a guest gets a room for some nights, and keeps every reservation.

| Word | Meaning here |
|---|---|
| Guest | A person who books a room; has a name and an email address |
| Stay | Check-in to check-out, half-open: 12–14 Nov = the nights of the 12th and 13th |
| Reservation | Guest + room number + stay + status, with an id such as R101 |
| Confirmed | The room is promised to this guest for these nights |
| Cancelled | The promise is withdrawn; the nights are free again |
| Book | A guest asks for a room for a stay; the answer is Accepted or Unavailable |
| Cancel | Withdraw a reservation, for example at the desk |
| Free rooms | The rooms with no Confirmed reservation that shares a night with the stay |

Rules this context owns:
- A room never has two Confirmed reservations that share a night.
- Check-out must be after check-in.
- Cancelling a reservation frees its nights for new bookings.

Needs from other contexts: the list of rooms (Rooms); from P17, the deposit (Payments).
Tells other contexts: ReservationConfirmed (Notifications).

## Payments

Job: takes deposits and records whether they were paid.

| Word | Meaning here |
|---|---|
| Deposit | 30% of the stay's price, taken when the guest books |
| Paid | The deposit was taken successfully |
| Declined | The deposit was refused (for example the card was declined) |

Rules this context owns:
- The deposit is 30% of the stay's price.
- Only a Paid deposit can be refunded.

Needs from other contexts: the nightly price (Rooms).
Tells other contexts: Paid or Declined, as the answer to "take a deposit" (Reservations).

## Notifications

Job: tells guests what happened, by email or SMS.

| Word | Meaning here |
|---|---|
| Confirmation message | The email or SMS that tells the guest "R101 is confirmed: room R7, 12–14 Nov" |
| Sent | The message arrived at the guest's provider |
| Failed | The message could not be sent; it is recorded and reported |

Rules this context owns:
- A failed message is recorded as Failed and never changes the reservation.

Needs from other contexts: nothing (it only reacts to ReservationConfirmed).
Tells other contexts: nothing.

## Same word, different meaning

| Word | Rooms | Reservations | Payments | Notifications |
|---|---|---|---|---|
| Room | R8: Deluxe, nightly price, out of service | Just the number R8 on a reservation | Not used | Text in the message: "Room R8" |
| Status | In service / out of service | Confirmed / Cancelled | Paid / Declined | Sent / Failed |
| Cancel | Take a room off sale | Withdraw a reservation | Refund a deposit | Not used |

If Notifications could change a reservation's status to Failed, a broken email provider would overwrite Confirmed, Maya would lose R7 because of a message, and rule R6 (a failed message never changes the booking) would be broken.

## Rule owners

| Card | Rule | Owner | Why this owner |
|---|---|---|---|
| 1 | A room never has two Confirmed reservations that share a night. | Reservations | It keeps every reservation of the room, so it can check them all together. |
| 2 | Check-out must be after check-in. | Reservations | The stay is its word, and it refuses wrong dates before anything else. |
| 3 | Cancelling a reservation frees its nights for new bookings. | Reservations | Only Confirmed reservations block a room; Reservations keeps the status. |
| 4 | A room that is out of service is not offered to guests. | Rooms | It knows which rooms are on sale. |
| 5 | The nightly price depends on the room type (Deluxe costs more than Standard). | Rooms | It keeps each room's type and price. |
| 6 | The deposit is 30% of the stay's price. | Payments | Money rules belong to Payments; it asks Rooms for the nightly price. |
| 7 | Only a Paid deposit can be refunded. | Payments | It keeps the payment status. |
| 8 | A failed message is recorded as Failed and never changes the reservation. | Notifications | It keeps the message status (rule R6). |

## Between contexts

### Reservations → Rooms: which rooms exist? (question)

Sent when: a guest searches for free rooms or books a room.

What Reservations sends: the question "which rooms exist?" (no fields).

The answer and its fields: a list of rooms; for each room the number and the type (R7 Standard, R8 Deluxe).

Never crosses: Reservations' list of reservations. Rooms never asks about reservations, so there is no arrow back.

### Reservations → Payments: take a deposit (question, from P17)

Sent when: a guest books a room (from P17, when the booking becomes a chain of steps).

What Reservations sends:
- reservationId: R101
- amount: 30% of the stay's price

The answer and its fields: Paid or Declined. Reservations decides what that answer means for the booking.

Never crosses: whether the room is free. Payments owns money only and never decides if a room is free.

### Reservations → Notifications: ReservationConfirmed (event)

Sent when: a reservation is saved as Confirmed.

Fields:
- reservationId: R101
- guestEmail: maya@example.com
- roomNumber: R7
- checkIn: 2026-11-12
- checkOut: 2026-11-14

Reservations does not wait for an answer. A failed message never changes R101 (rule R6).

Never crosses: Reservations' list of reservations. Notifications never reads it.