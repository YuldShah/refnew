import os


MAIN_MENU_TEXT = """<b>🎓 Assalomu alaykum, {user_name}!</b>
<blockquote>SAT Math bepul marafoni haqida to‘liq va rasmiy ma’lumot bilan tanishing.</blockquote>
<b>👇👇Quyidagi menyudan kerakli bo‘limni tanlang👇👇</b>"""

PARTICIPATION_PHOTO_ID = os.getenv(
    "PARTICIPATION_PHOTO_ID",
    "REPLACE_ME_PARTICIPATION_PHOTO_ID",
)
TURBO_INFO_PHOTO_ID = os.getenv(
    "TURBO_INFO_PHOTO_ID",
    "REPLACE_ME_TURBO_INFO_PHOTO_ID",
)
REFERRAL_PHOTO_ID = os.getenv(
    "REFERRAL_PHOTO_ID",
    "REPLACE_ME_REFERRAL_PHOTO_ID",
)
PRIZES_PHOTO_ID = os.getenv(
    "PRIZES_PHOTO_ID",
    "REPLACE_ME_PRIZES_PHOTO_ID",
)

PARTICIPATION_CAPTION = """🎯 <b>Bepul Turbo Marafonda qatnashish sharti!</b>
<blockquote>1️⃣ <b>Bot sizga shaxsiy taklif havolasini taqdim etadi.</b>
Siz ushbu havolani kamida <b>3 nafar SAT imtihoniga tayyorlanayotgan tanishlaringizga</b> yuborishingiz kerak bo‘ladi.
Ular <b>sizning havolangiz orqali botga kirsa</b>, har biri qoshilgan odam uchun sizga <b>1 balldan</b> beriladi.</blockquote>
<blockquote>2️⃣ <b>Agar ballaringiz 3 yoki undan ko‘p bo‘lsa</b>,
<b>“Ballarim”</b> bo‘limi orqali siz uchun <b>maxsus yopiq kanal va guruhga qo‘shilish</b> imkoniyatiga ega bo‘lasiz.</blockquote>
🚫 <b>Agar ballaringiz 3 dan kamaysa</b>, siz <b>avtomatik tarzda</b> yopiq guruh va kanaldan <b>chetlatilasiz</b>.
📈 <b>Iloji boricha ko‘proq ball yig‘ishingiz tavsiya etiladi.</b>
<blockquote>📌 <b>Taklif havolangizni SAT’ning matematika qismi bilan shug‘ullanayotgan tanishlaringizga yuboring!</b></blockquote>
✅ <b>Tayyor bo‘lsangiz</b>, menyudan <b>“🔗 Taklif havolasi 🔗”</b> tugmasini bosing va do‘stlaringizni taklif qiling!"""

TURBO_INFO_CAPTION = """<b>Men</b> Asatullayev Elbek
<blockquote>SAT math o‘qituvchisi va SAT Math dan 5 marta 800/800 maksimal natija egasi sifatida sizlarni SAT Elbek tomonidan tashkil etilayotgan.</blockquote>
Darslarni 0 dan o'qib o'rganishiz mumkin.

<b>SAT Math Turbo Marafonga taklif qilaman 🚀</b>
<blockquote>🔥 Turbo formatdagi intensiv darslarda qatnashing
🎁 SAT $111 registratsiya to‘lovi uchun BEPUL vaucherga ega bo‘ling</blockquote>

<b>💡 Bonus imkoniyat:</b>
<blockquote>Agarda siz darslar va vazifalarda muntazam qatnashsangiz
💸 <b>TOP 5 reytingga kirsangiz — SAT registratsiya summasi to‘liq SAT Elbek tomonidan to‘lab beriladi!</b></blockquote>"""

REFERRAL_CAPTION = """Men Elbek Asatullayev<b>, SAT Math o‘qituvchisi</b>,
<blockquote>🎯 <b>SAT Math’dan 5 marta 800/800 maksimal natija egasi</b> sifatida sizlarni
<b>SAT Elbek</b> tomonidan tashkil etilgan
<b>SAT Math Turbo Marafon</b>ga taklif etaman 🚀</blockquote>

📊 <b>Hozirga qadar:</b>
<blockquote>✅ <b>100000 ga yaqin matematika ustozlariga</b> dars berganman,
👉 ularni mutloq <b>noldan 50%+ ustama natijaga</b> olib chiqqanman
🏆 100<b> dan ortiq o‘quvchini</b>
👉 <b>SAT Math 800/800 maksimal natijaga</b> olib chiqqanman</blockquote>

🔥 <b>Turbo darslarimizda qatnashing</b>
<blockquote>🎁 <b>SAT imtihoni uchun $111 registratsiya summasiga TEKIN vaucher</b> qo‘lga kiriting</blockquote>

💡 <b>Bonus imkoniyatlar:</b>
<blockquote>Agar siz <b>darslar va vazifalarda o‘z vaqtida qatnashib</b>,
<b>TOP 5 reyting</b>ga kirsangiz —
💸 <b>SAT registratsiya summasi to‘liq $555 miqdorida</b>
<b>SAT Elbek tomonidan qoplab beriladi!</b></blockquote>

🚀 <b>Agar siz ham Turbo Marafon guruhimizga qo‘shilmoqchi bo‘lsangiz</b> —
botga <a href="{referral_link}"><b>“Start”</b></a> bering va joyingizni band qiling 👇

<blockquote>⚠️ <b>Joylar soni cheklangan, shoshiling!</b></blockquote>
{referral_link}"""

REFERRAL_FOLLOWUP_TEXT = """<b>👆 Yuqoridagi sizning taklif havolangiz.</b>
<blockquote>👑 Taklif havolangiz orqali botimizga 3 va undan ortiq do'stlaringizni taklif qiling va Olimpiada kanal va guruhimizga qo'shilish imkoniyatini qo'lga kiriting!</blockquote>
<b>❗️SHOSHILING! Jami bo'lib 200 ta joy ajratilgan🤝</b>"""

POINTS_TEXT = """<b>📈 </b><a href="https://t.me/asatullayevelbek"><b>SAT offline admin </b></a><b> sizning ballaringiz: {points} ball.</b>
<blockquote>‼️ Siz taklif havolangiz orqali qo'shilgan odam kanallardan obunani bekor qilsa sizga shu odam uchun berilgan ball qaytarib olinadi!</blockquote>
<b>✅ Hisobingizdagi ballar 3 va undan yuqori ballga ega bo‘lgandan so‘ng yopiq kanal va guruhimizga qo‘shilishingiz mumkin bo‘ladi.</b>"""

PRIZES_CAPTION = """🚀 <b>Turbo Marafon = bilim + real sovrinlar!</b>
<blockquote><b>Turbo Marafonda qatnashib</b> siz nafaqat <b>bilim va yuqori natija</b>,
balki <b>SAT imtihoni uchun $111 registratsiya summasini yutib olish</b> imkoniyatiga ham ega bo‘lasiz 🎯</blockquote>

🏆 <b>Mukofotlar:</b>
<i><b>Turbo Marafonda yuqori natija ko‘rsatgan</b> ustozlar va o‘quvchilar orasidan
👉 </i><i><b>jami 5 nafar ishtirokchi</b> uchun</i>
<blockquote>💰 <b>Mart oyidagi SAT registratsiya summasi ($111)</b>
<b>SAT Elbek tomonidan TO‘LIQ qoplab beriladi!</b></blockquote>

🔥 <b>Qo‘shimcha imkoniyat:</b>
<b><i>Yana 10 nafar ishtirokchi</i></b>
<blockquote>📘 <b>SAT Mock Turbo guruhlariga 50% chegirma</b> asosida qabul qilinadi.</blockquote>"""

ACCESS_READY_TEXT = """<b>✅ Sizda yetarli ball bor.</b>
<blockquote>Quyidagi bir martalik havolalar orqali yopiq kanal va guruhlarga qo‘shiling.</blockquote>"""


def media_is_configured(media_id: str) -> bool:
    return bool(media_id) and not media_id.startswith("REPLACE_ME_")
