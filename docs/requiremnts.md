# Requirements: hotel booking app, version 1

## R1 · Search
Mehmon yoki qabulxona xodimi berilgan sanalar uchun bo'sh xonalar ro'yxatini ko'ra oladi.
Check: bo'sh mehmonxona, 12–14 noyabr → R7, R8.

## R2 · Book
Mehmon yoki qabulxona xodimi bo'sh xonani bron qila oladi. Ilova bron raqamini (reservation id) qaytaradi.
Check: Maya R7 ni 12–14 noyabrga bron qiladi → Accepted R101.

## R3 · No clash
Bitta xonada bir xil tunga ikkita Confirmed bron bo'lmaydi. Chiqish sanasi kirish sanasidan keyin bo'lishi kerak.
Check: Omar R7 ni 13–15 ga so'raydi → Unavailable. 15–15 → InvalidDates.

More examples:
- Maya R7 12–14 → Confirmed (12 va 13 tunlar)
- Omar R7 13–15 → Unavailable (13-tun)
- Nora R7 14–16 → Accepted (umumiy tun yo'q)
- R8 20–22 noyabrga band. R8 22–24 so'raladi → Accepted (22-kun chiqish kuni)
- R8 20–22 noyabrga band. R8 21–23 so'raladi → Unavailable (21-tun)

## R4 · Cancel
Bronni bekor qilish mumkin. U Cancelled holatida saqlanadi va xonani endi band qilmaydi.
Check: Maya R101 ni bekor qiladi → R7 12–14 uchun yana bo'sh.

## R5 · View
Bronni uning raqami bo'yicha topish mumkin.
Check: R101 → Maya, R7, 12–14 noyabr, Confirmed.