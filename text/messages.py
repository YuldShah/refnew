MESSAGES = {
    'uz': {
        'welcome': """<b>🎓 Assalomu alaykum,</b> {link_to_user}!
<blockquote>Sizni May SAT matematika uchun BEPUL Turbo Marafonimizga taklif qilamiz!</blockquote>
✅ Batafsil ma'lumot uchun "📋 SAT marafon haqida 📋" tugmasini bosing""",
        'referral_welcome': "Siz <b>{referrer}</b> tomonidan taklif qilindingiz! 🎉",
        'already_registered': """Siz allaqachon botda ro'yxatdan o'tgansiz!""",
        'invalid_referral': "Noto'g'ri taklif havolasi!",
        'subscription_required': "Botdan foydalanish uchun bizning barcha kanallarimizga obuna bo'ling:",
        'not_subscribed': "Siz hali ham barcha kanallarga obuna bo'lmagansiz!",
        'our_chats_folder': "Bizning kanallar papkasi 📁",
        'subscribe_button': "Obuna bo'lish ✅",
        'check_subscription': "Obunani tekshirish ✅",
        'subscription_confirmed': "✅ Tabriklaymiz! Siz barcha bizning kanallarga obuna bo'ldingiz va botdan bemalol foydalanishingiz mumkin!",
        'referral_system': "Taklif tizimi 📊",
        'valid_referrals': "Tasdiqlangan takliflar: <b>{count}</b>",
        'pending_referrals': "Kutilayotgan takliflar: <b>{count}</b>",
        'your_referral_link': "Sizning taklif havolangiz:\n<code>{link}</code>",
        'admin_panel': "👨‍💼 Admin panelga xush kelibsiz!",
        'admin_top_referrers': "🏆 Top 10",
        'admin_user_lookup': "🔍 Qidirish",
        'admin_export_data': "📊 Excel",
        'admin_stats': "📈 Statistika",
        'admin_manage_access': "🔐 Majburiy chatlar",
        'back_to_admin_menu': "🏘 Bosh menyu",
        'admin_user_not_found': "⚠️ Foydalanuvchi topilmadi",
        'admin_enter_user_id': "🔍 Qidirish uchun foydalanuvchi ID raqamini kiriting:",
        'admin_user_info': "<b>Foydalanuvchi ma'lumotlari:</b>\n\n👤 ID: {telegram_id}\n📝 Ism: {full_name}\n📱 Username: @{username}\n🔗 Taklif kodi: {referral_code}\n📅 Qo'shilgan sana: {joined_at}\n\n<b>Referral statistikasi:</b>\n\n✅ Tasdiqlangan takliflar: {valid_referrals}\n⏳ Kutilayotgan takliflar: {pending_referrals}",
        'admin_export_success': "✅ Foydalanuvchilar ma'lumotlari muvaffaqiyatli eksport qilindi!",
        'admin_export_error': "⚠️ Eksport qilishda xatolik yuz berdi.",
        'admin_top_referrers_title': "🏆 <b>TOP 10 Referrerlar:</b>\n\n",
        'admin_top_referrer_item': "{position}. {full_name} (@{username}) - {count} ta taklif",
        'manage_channels': "Kanallarni boshqarish",
        'add_channel': "Kanal qo'shish",
        'remove_channel': "Kanalni o'chirish",
        'channel_added': "Kanal muvaffaqiyatli qo'shildi!",
        'channel_removed': "Kanal o'chirildi!",
        'send_channel_info': "Kanal ID, nomi va username kiriting:",
        'invalid_format': "Noto'g'ri format!",
        'back': "⬅️ Orqaga",
        'language_settings': "Til sozlamalari 🌐",
        'current_language': "Joriy til: <b>O'zbek tili</b> 🇺🇿",
        'switch_to_english': "Switch to English 🇺🇸",
        'language_changed': "Til muvaffaqiyatli o'zgartirildi! 🎉",
        'unexpected_error': "Kutilmagan xatolik yuz berdi! ⚠️\nIltimos, keyinroq urinib ko'ring.",        'channel_validation_error': "Kanalni tekshirishda xatolik yuz berdi.",
        'channel_not_accessible': "Bot ushbu kanalga kirish huquqiga ega emas.",
        'add_bot_as_admin': "Botni kanal administratori sifatida qo'shing.",
        'register_first': "Iltimos, avval ro'yxatdan o'ting.\n\n/start /start /start",
        
        # Main menu buttons
        'rules_button': "‼️ Marafonda qatnashish sharti ‼️",
        'get_reward_button': "📊Ballarim📊",
        'my_referral_link_button': "🔗Taklif havolasi🔗",
        'my_stats_button': "📊Ballarim📊",
        'about_olympiad_button': "📋 SAT marafon haqida 📋",
        'rewards_button': "🎁 Sovrinlar ⭐️",
        'share_referral_link': "🔗 Taklif havolasini ulashish",
        'back_to_menu': "🔙 Bosh menyuga qaytish",
        'refresh_stats': "🔄 Yangilash",
        'search_user': "🔍 Qidirish",
        'top_10_referrers': "🏆 Top 10",
        'export_my_data': "📊 Eksport",
        'stats_up_to_date': "📊 Statistika yangilangan",
        
        # Manage access messages
        'mandatory_channels_btn': "📋 Majburiy kanallar",
        'manual_access_btn': "👤 Qo'lda boshqarish",
        'add_channel_btn': "➕ Kanal qo'shish",
        'reset_all_channels_btn': "🔄 Hammasini o'chirish",
        'add_user_access_btn': "✅ Ruxsat berish",
        'remove_user_access_btn': "❌ Ruxsatni olib qo'yish",
        'back_btn': "⬅️ Orqaga",
        'confirm_btn': "✅ Tasdiqlash",
        'cancel_btn': "❌ Bekor qilish",
        
        # Rules content (participation conditions)
        'rules_content': """🎯 <b>Bepul Turbo SAT Marafonida ishtirok eting!</b>
<blockquote>1️⃣ Bot sizga shaxsiy taklif havolasini taqdim etadi. Siz ushbu havolani kamida 3 nafar SAT imtihoniga tayyorlanayotgan tanishlaringizga yuborishingiz kerak bo'ladi. Ular sizning havolangiz orqali botga kirsa, har biri uchun sizga 1 balldan beriladi.
2️⃣ Sizning <b>ballaringiz 3 va undan ko'p</b> bo'lsa, Ballarim bo'limi orqali siz uchun maxsus yopiq kanal va guruhga qo'shilish imkoniyatiga ega bo'lasiz.</blockquote>
🚫 <b>Ballaringiz 3 dan kamayib ketsa, avtomatik tarzda guruh va kanaldan chetlatilasiz.</b>
<blockquote>📌 Taklif havolangizni matematika bilan shug'ullanayotgan tanishlaringizga yuborishga harakat qiling!</blockquote>
✅ Tayyor bo'lsangiz, menyudan "🔗 <b>Taklif havolasi</b> 🔗" tugmasini bosing va do'stlaringizni taklif qiling!""",

        'reward_available': """🎉 <b>Tabriklaymiz!</b>

🎯 <i>Siz {required_referrals} ta tasdiqlangan foydalanuvchilarni taklif qildingiz! Endi siz darslarimizda qatnasha olasiz!</i>

👇 Quyida sizga darslarimiz bo'lib o'tadigan kanal va guruhlar havolalari berilgan.

<blockquote>Yodda tuting, ushbu havolalar orqali faqat bir kishi kanallar va guruhlarga qo'shilishi mumkin.</blockquote>
""",

        'reward_not_available': """
🎯 Darslarimizga qo'shilish uchun {required_referrals} ta SAT topshirmoqchi bo'lgan tanishingizni botga taklif qilishingiz kerak.

<blockquote>✅ Siz hozircha {current_referrals} ta foydalanuvchini taklif qildingiz. 
📢 Yana {remaining_referrals} ta do'stingizni taklif qiling!</blockquote>

✍️ Yodda tuting, taklif qilgan tanishlaringiz ham bizning barcha kanallarimizga a'zo bo'lishlari shart!""",

        'reward_eligible_notification': """🎉 <b>Tabriklaymiz!</b>

🎯 Siz {required_referrals} ta tasdiqlangan taklif to'pladingiz!
""",
        
        # Referral link messages
        'referral_link_message': """<b>Deyarli hamma ustama olib boldi. Sizda esa hali ham tayyorgarlik yaxshi emas.
Bizda esa siz uchun ajoyib yechim bor.</b>
<i>Jamoamiz o'z</i> ishining ustasi
<blockquote>Elbek Asatullayev
<b>SAT math ketma-ket 4 marta 800/800 maximal ball 🔥
SAT umumiy natija 1550/1600 ⭐️
IELTS overall 7.5/9.0 ball 📌
Agar sizning ingliz tili darajangiz 0 bolsa, sizga ingliz tili o'rganishni eng oson usullarini biz o'rgatamiz.
Ayniqsa matnli masalalarga kelganda boshqa kurslardan farqini sezasizlar. ‼️</b></blockquote>

<blockquote>Sizlarni MAY SAT BEPUL Turbo  Marafon yopiq guruh va kanalimizga taklif etamiz

📊So'nggi 2 yil ichida kurslarimizda  4000+ ustozlar va o'quvchilarimiz Xalqaro Sertifikatlarda maximal natija qayd etdi.
Ularning qatorida esa navbat endi sizniki bo'lishi shart!

🟢 Taklif havola tugmasini bosing!</blockquote>
🟢 <b>Agar siz ham Turbo Marafon guruhimizga qo'shilmoqchi bo'lsangiz — botga </b><a href="https://t.me/satbepulbot"><b>Start</b></a><b> bering va joyingizni band qiling!</b>
<blockquote>⚠️ Joylar soni kam qolmoqda 👇</blockquote>

<code>{link}</code>
""",
        'referral_link_error': "Taklif havolasini olishda xatolik yuz berdi.",
        
        # About olympiad message
        'about_olympiad': """📢 <b>Assalomu alaykum, hurmatli matematika ustozlar va o'quvchilar!</b>

SAT imtixonining matematika qismidan <i>anchadan beri tayyorgarlik ko'rayapsiz lekin natijalar siz xohlagan darajada emasmi?</i>

📌 <b>Unda sizni May SAT matematika uchun BEPUL Turbo Marafonimizga taklif qilaman!</b>
<blockquote>⚡️O'qituvchimiz— Bir nechta xalqaro sertifikatlar sohibi

<b>ELBEK Asatullayev
SAT Math ketma-ket 4x (800/800)
SAT Umumiy natija (1550/1600)
IELTS (7.5/9.0)
Dekabr imtixonning ozida SAT matematikadan maximal 25 ta 800/800 natija
So'nggi 2 yil ichida kurslarimizda  4000+</b> ustozlar Xalqaro Sertifikatlarda maximal natija qayd etdi.
Ularning qatorida esa navbat endi sizniki bo'lishi shart!

<b>Ustozimiz</b> o'z soxasi ustasi va sizni imtixongacha puxta va hotirjam tayyor bolishingizda yaqindan yordam beradi.</blockquote>
🎯 <i>Agar siz ham jonli darslarimizga qatnashib, darslarimizdan namunalar ko'rib,  kursimizga qo'shilmoqchi bo'lsangiz.
Marafon shartlarini bajaring va joyingizni oldindan band eting.</i>

Marafonda qatnashish uchun "‼️ <b>Marafonda qatnashish sharti </b>‼️" tugmasini bosing va batafsil ma'lumotni oling!""",
        
        # Photo file_ids (placeholders to fill later)
        'rewards_photo': "",
        'referral_link_photo': "",
        'sat_opportunities_photo': "",
        
        # Rewards/prizes message
        'rewards_info': """🏆<b> Marafonda sizni nafaqat bilim, balki KATTA imkoniyatlar ham kutmoqda!</b>
<blockquote><i>📌 Marafon guruhida faol qatnashib, vazifalarni bajargan  eng  yuqori natija qayd etgan 3 ta ustozlarimizga imtixon</i> harajatlari toliq qoplanib beriladi (111$+Turbo kursimiz narxi)</blockquote>
<blockquote>Shoshmang, bu Hali hammasi e,marafonga qatnashib, vazifalarni o'z vaqtida bajarib aktivlik ko'rsatgan Top-7 ishtirokchilarga esa Mart kursi uchun  💯 foizlik vaucherlar taqdim etiladi</blockquote>
🎯<b>Shoshiling,  sovg'alardan  biri aynan sizniki bo'lishi mumkin.</b>""",
        
        # User stats messages        
        'user_stats_message': """<b>📈 Sizning ballaringiz: {valid_referrals} ball.</b>
<blockquote>‼️ Siz taklif havolangiz orqali qo'shilgan odam kanallardan obunani bekor qilsa sizga shu odam uchun berilgan ball qaytarib olinadi!</blockquote>
<b>✅ Hisobingizdagi ballar 3 balldan yuqori qiymatga ega bo‘lgandan so‘ng yopiq kanal va guruhimizga qo‘shilishingiz mumkin bo‘ladi.</b>
""",
        'sat_opportunities': """<b>Hozirda SAT sizga qanday imkoniyatlar bermoqda.
1) Agarda siz matematika o'qituvchisi bolsangiz SAT imtixonining matematika qismidan eng kamida 700/800 natija orqali 3 yilga 50% ustamani naqd qilasiz

2) Agarda siz maktab o'quvchisi bolsangiz vazirlar mahkamasining yaqinda  qabul qilgan qaroriga ko'ra SAT imtixonidan umumiy 1200+ natija orqali davlat universitetlariga 100% grandni qo'lga kiritasiz</b>""",
        'referrals_validated': """🎉 <b>Yangilik!</b> Do'stlaringizdan {count} ta yangi taklif tasdiqlandi!""",
        
        # Referrer notification messages
        'referrer_new_user_subscribed': """🎉 <b>Yangi foydalanuvchi!</b>

👤 {user_name} sizning taklifingiz orqali botga qo'shildi va bizning barcha kanallarimizga obuna bo'ldi!

✅ Bu taklif tasdiqlangan takliflar ro'yxatiga qo'shildi.""",
        
        'referrer_new_user_pending': """🔔 <b>Yangi foydalanuvchi!</b>

👤 {user_name} sizning taklifingiz orqali botga qo'shildi.

⏳ Taklif qilingan foydalanuvchi bizning kanallarga obuna bo'lgandan so'ng taklif tasdiqlanadi.""",
        
        'referrer_user_subscribed': """🎉 <b>Taklif tasdiqlandi!</b>

👤 {user_name} bizning kanallarga obuna bo'ldi!

✅ Bu taklif endi tasdiqlangan takliflar ro'yxatida.""",
    },
    'en': {
        'welcome': "Welcome to the bot! 🎉",
        'referral_welcome': "You were invited by <b>{referrer}</b>! 🎉",
        'already_registered': "You are already registered!",
        'invalid_referral': "Invalid referral link!",
        'subscription_required': "Subscribe to all mandatory channels to use the bot:",
        'our_chats_folder': "Our Chats Folder 📁",
        'subscribe_button': "Subscribe ✅",
        'check_subscription': "Check Subscription ✅",
        'not_subscribed': "You are still not subscribed to all channels!",
        'subscription_confirmed': "✅ Congratulations! You have subscribed to all mandatory channels!",
        'referral_system': "Referral System 📊",
        'valid_referrals': "Valid referrals: <b>{count}</b>",
        'pending_referrals': "Pending referrals: <b>{count}</b>",
        'your_referral_link': "Your referral link:\n<code>{link}</code>",
        'admin_panel': "Admin Panel 👨‍💼",
        'admin_top_referrers': "🏆 Top 10 referrers",
        'admin_user_lookup': "🔍 Find user by ID",
        'admin_export_data': "📊 Export user data",        'admin_stats': "📈 Statistics",
        'admin_manage_access': "🔐 Manage Access",
        'back_to_admin_menu': "🏘 Main menu",
        'admin_user_not_found': "⚠️ User not found",
        'admin_enter_user_id': "🔍 Enter Telegram user ID to search:",
        'admin_user_info': "<b>User Information:</b>\n\n👤 ID: {telegram_id}\n📝 Name: {full_name}\n📱 Username: @{username}\n🔗 Referral code: {referral_code}\n📅 Joined: {joined_at}\n\n<b>Referral statistics:</b>\n\n✅ Confirmed referrals: {valid_referrals}\n⏳ Pending referrals: {pending_referrals}",
        'admin_export_success': "✅ User data exported successfully!",
        'admin_export_error': "⚠️ Error exporting data.",
        'admin_top_referrers_title': "🏆 <b>TOP 10 Referrers:</b>\n\n",
        'admin_top_referrer_item': "{position}. {full_name} (@{username}) - {count} referrals",
        'manage_channels': "Manage Channels",
        'add_channel': "Add Channel",
        'remove_channel': "Remove Channel",
        'channel_added': "Channel added successfully!",
        'channel_removed': "Channel removed!",
        'send_channel_info': "Send channel ID, title and username:",
        'invalid_format': "Invalid format!",
        'back': "⬅️ Back",
        'language_settings': "Language Settings 🌐",
        'current_language': "Current language: <b>English</b> 🇺🇸",
        'switch_to_uzbek': "O'zbek tiliga o'tish 🇺🇿",
        'language_changed': "Language changed successfully! 🎉",
        'unexpected_error': "An unexpected error occurred! ⚠️\nPlease try again later.",        'channel_validation_error': "Error occurred while validating channel.",
        'channel_not_accessible': "Bot doesn't have access to this channel.",
        'add_bot_as_admin': "Add the bot as an admin to the channel.",
        
        # Main menu buttons
        'rules_button': "📋 Rules",
        'get_reward_button': "🎁 Get Reward",
        'my_referral_link_button': "🔗 My Referral Link",        'my_stats_button': "📊 My Stats",        'back_to_menu': "🔙 Back to Menu",
        'refresh_stats': "🔄 Refresh",
        'search_user': "🔍 Search",
        'top_10_referrers': "🏆 Top 10",
        'export_my_data': "📊 Export",
        'stats_up_to_date': "📊 Stats updated",
        
        # Manage access messages
        'mandatory_channels_btn': "📋 Mandatory Channels",
        'manual_access_btn': "👤 Manual Control",
        'add_channel_btn': "➕ Add Channel",
        'reset_all_channels_btn': "🔄 Reset all",
        'add_user_access_btn': "✅ Grant Access",
        'remove_user_access_btn': "❌ Revoke Access",
        'back_btn': "⬅️ Back",
        'confirm_btn': "✅ Confirm",
        'cancel_btn': "❌ Cancel",
        
        # Rules content (placeholder)
        'rules_content': """📋 <b>Bot Rules</b>

🔹 Subscribe to all mandatory channels to use the bot
🔹 Share your referral link with friends
🔹 Get rewards for each confirmed referral
🔹 Spam and inappropriate behavior is prohibited

Complete rules will be written here...""",
          # Reward content
        'reward_content': """🎁 <b>Rewards</b>

🎯 Special group access after {required_referrals} confirmed referrals!

📊 Current status:
✅ Confirmed referrals: {current_referrals}
⏳ Remaining: {remaining_referrals}

Refer {remaining_referrals} more friends and get your reward! 🚀""",

        'reward_available': """🎉 <b>Congratulations!</b>

🎯 You have collected {required_referrals} confirmed referrals!

🎁 Your reward: Special group access!

👇 Click the link below:
{reward_link}

🚀 Exciting content and bonuses are waiting in the group!""",

        'reward_not_available': """🎁 <b>Rewards</b>

🎯 You need {required_referrals} confirmed referrals to access the special group.

📊 Current status:
✅ Confirmed referrals: {current_referrals}
⏳ Remaining: {remaining_referrals}

📢 Refer {remaining_referrals} more friends and get your reward!

💡 How to refer:
1. Press "📊 Statistics" button
2. Copy your referral link
3. Send to your friends""",

        'reward_already_accessed': """🎁 <b>Reward received!</b>

✅ You have already received your reward and joined the special group!

🚀 But keep going! Refer more friends and expand our community!

📊 Track your results in the "Statistics" section.""",

        'reward_eligible_notification': """🎉 <b>Congratulations!</b>

🎯 You have collected {required_referrals} confirmed referrals!

🎁 A special reward is ready for you! Press the "🎁 Get Reward" button and claim your prize!

💰 Access to the special group is waiting for you!""",
        
        # Referral link messages
        'referral_link_message': """🔗 <b>Your referral link:</b>

<code>{link}</code>

Share this link with your friends and get rewards! 💰""",        'referral_link_error': "Error getting referral link.",
        
        # User stats messages
        'user_stats_message': """📊 <b>Your Statistics:</b>

👥 Total referrals: <b>{total_referrals}</b>
✅ Confirmed referrals: <b>{valid_referrals}</b>
⏳ Pending referrals: <b>{pending_referrals}</b>

Keep going and earn more rewards! 🎯""",
        'referrals_validated': """🎉 <b>News!</b> {count} new referrals have been confirmed from your friends!""",
        
        # Referrer notification messages
        'referrer_new_user_subscribed': """🎉 <b>Yangi foydalanuvchi!</b>

👤 {user_name} sizning taklifingiz orqali botga qo'shildi va bizning barcha kanallarimizga obuna bo'ldi!

✅ Bu taklif tasdiqlangan takliflar ro'yxatiga qo'shildi.""",
        
        'referrer_new_user_pending': """🔔 <b>Yangi foydalanuvchi!</b>

👤 {user_name} sizning taklifingiz orqali botga qo'shildi.

⏳ Hozircha bizning kanallarimizga obuna bo'lishi kutilmoqda. Obuna bo'lgandan so'ng taklif tasdiqlanadi.""",
        
        'referrer_user_subscribed': """🎉 <b>Taklif tasdiqlandi!</b>

👤 {user_name} bizning kanallarimizga obuna bo'ldi!

✅ Bu taklif endi tasdiqlangan takliflar ro'yxatida.""",
    }
}

def get_text(key: str, lang: str = 'uz', **kwargs) -> str:
    text = MESSAGES.get(lang, MESSAGES['uz']).get(key, key)
    return text.format(**kwargs) if kwargs else text

async def get_user_text(key: str, user_id: int, db, **kwargs) -> str:
    lang = await db.get_user_language(user_id)
    return get_text(key, lang, **kwargs)
