import os


MAIN_MENU_TEXT = """<b>🎓 Assalomu alaykum, {user_name}!</b>
<blockquote>SAT Math bepul marafoni haqida to‘liq va rasmiy ma’lumot bilan tanishing.</blockquote>
<b>👇👇Quyidagi menyudan kerakli bo‘limni tanlang👇👇</b>"""

REGISTRATION_NAME_PROMPT = """<b>📝 Ro‘yxatdan o‘tish boshlandi!</b>
<blockquote>Botdan to‘liq foydalanish uchun quyidagi ma’lumotlarni ketma-ket yuboring.</blockquote>
<b>1-qadam:</b> Ism va familiyangizni yuboring."""

REGISTRATION_NAME_INVALID_TEXT = """<b>⚠️ Ism va familiya qabul qilinmadi.</b>
<blockquote>Iltimos, ism va familiyangizni matn ko‘rinishida va to‘liq yuboring.</blockquote>"""

REGISTRATION_AGE_PROMPT = """<b>2-qadam:</b> Yoshingizni kiriting.
<blockquote>Yoshni faqat raqam bilan yuboring.</blockquote>"""

REGISTRATION_AGE_INVALID_TEXT = """<b>⚠️ Yosh noto‘g‘ri kiritildi.</b>
<blockquote>Iltimos, yoshingizni faqat raqam bilan yuboring.</blockquote>"""

REGISTRATION_AGE_RANGE_INVALID_TEXT = """<b>⚠️ Yosh noto‘g‘ri kiritildi.</b>
<blockquote>Iltimos, haqiqiy yoshingizni kiriting.</blockquote>"""

REGISTRATION_PHONE_PROMPT = """<b>3-qadam:</b> Telefon raqamingizni yuboring.
<blockquote>Pastdagi tugma orqali raqamingizni ulashing.</blockquote>"""

REGISTRATION_PHONE_INVALID_TEXT = """<b>⚠️ Telefon raqam qabul qilinmadi.</b>
<blockquote>Iltimos, pastdagi tugma orqali o‘zingizning telefon raqamingizni yuboring.</blockquote>"""

REGISTRATION_STATUS_PROMPT = """<b>4-qadam:</b> Ta’limdagi maqomingizni tanlang.
<blockquote>Quyidagi inline tugmalardan birini bosing.</blockquote>"""

REGISTRATION_STATUS_INVALID_TEXT = """<b>⚠️ Maqom tanlanmadi.</b>
<blockquote>Iltimos, ta’limdagi maqomingizni inline tugmalar orqali tanlang.</blockquote>"""

REGISTRATION_SAT_GOAL_PROMPT = """<b>5-qadam:</b> SAT sizga nimaga kerak?
<blockquote>Quyidagi variantlardan birini tanlang.</blockquote>"""

REGISTRATION_SAT_GOAL_INVALID_TEXT = """<b>⚠️ Variant tanlanmadi.</b>
<blockquote>Iltimos, SAT maqsadini tugmalar orqali tanlang.</blockquote>"""

REGISTRATION_COMPLETE_TEXT = """<b>✅ Rahmat!</b>
<blockquote>Ma’lumotlaringiz muvaffaqiyatli saqlandi.</blockquote>"""

REGISTRATION_PHONE_ACCEPTED_TEXT = """<b>✅ Telefon raqamingiz qabul qilindi.</b>
<blockquote>Keyingi qadamga o‘tamiz.</blockquote>"""

REGISTRATION_PHONE_SKIPPED_TEXT = """<b>3-qadam o‘tkazib yuborildi.</b>
<blockquote>Siz yuborgan telefon raqami: <b>{phone_number}</b></blockquote>
<b>Telefon raqamingiz saqlangan va qayta so‘ralmaydi.</b>"""

REGISTRATION_BACK_BUTTON_TEXT = "⬅️ Orqaga"
REGISTRATION_SHARE_PHONE_BUTTON_TEXT = "📱 Telefon raqamni yuborish"

REGISTRATION_STATUS_SELECTED_TEXT = """<b>4-qadam yakunlandi.</b>
<blockquote>Tanlangan maqom: <b>{option}</b></blockquote>"""

REGISTRATION_SAT_GOAL_SELECTED_TEXT = """<b>5-qadam yakunlandi.</b>
<blockquote>Tanlangan maqsad: <b>{option}</b></blockquote>"""

REGISTRATION_BACK_NAV_TEXT = """<b>↩️ Oldingi qadamga qaytdingiz.</b>"""

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

POINTS_TEXT = """<b>📈 {user_name}, sizning ballaringiz: {points} ball.</b>
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
