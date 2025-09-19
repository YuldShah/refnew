MESSAGES = {
    'uz': {
        'welcome' : """👋 Assalomu alaykum, <b>{link_to_user}</b>, yaxshimisiz?

⚡️Sizni koʻrib turgan turganimdan xursandman🤩

Siz SAT sertifikat olish uchun muhim qadam tashladingiz!

📌Siz bilan SAT math qismiga tayorlanamiz, quyidagi menyudan kerakli boʻlimni tanlang👇👇👇👇""",
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
        'unexpected_error': "Kutilmagan xatolik yuz berdi! ⚠️\nIltimos, keyinroq urinib ko'ring.",        
        'channel_validation_error': "Kanalni tekshirishda xatolik yuz berdi.",
        'channel_not_accessible': "Bot ushbu kanalga kirish huquqiga ega emas.",
        'add_bot_as_admin': "Botni kanal administratori sifatida qo'shing.",
        'register_first': "Iltimos, avval ro'yxatdan o'ting.\n\n/start /start /start",
        
        # Main menu buttons
        'rules_button': "📋 Qoidalar",
        'get_reward_button': "🚀 Kirish huquqini olish",
        'my_referral_link_button': "🔗 Mening taklif havolam",        
        'my_stats_button': "📊 Mening statistikam",
        'share_referral_link': "🔗 Referral havolani ulashish",
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
        
        # Rules content (placeholder)
        'rules_content': """📋 <b>Bot qoidalari</b>

🔹 Botdan foydalanish uchun barcha majburiy kanallarga obuna bo'ling
🔹 Taklif havolangizni do'stlaringiz bilan ulashing
🔹 Har bir tasdiqlangan taklif uchun mukofot oling
🔹 Spam va noto'g'ri harakatlar taqiqlanadi

Bu yerda qoidalar to'liq yoziladi...""",

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
        'referral_link_message': """
<b>Ingliz tili 0 darajada bo'lgan lekin Xalqaro SAT sertifikati orqali 3 yil davomida 50% ustama olishni xohlaganlar uchun SAT ELBEK tomonidan barchaga manfaatli loyihaga start bermoqdamiz!

Bizni asosiy maqsadimiz o'qituvchilarni shu serifikat ni olib oz-moz bolsada oilaga qoshimcha rizq olib kirishiga sababchi bolishdir


O'qituvchi: 
Elbek Asatullayev 3x SAT Math score 800/800</b>

1⃣
<blockquote>Oxirgi 2 yil davomida Ingliz tili mutloqo 0 Dan 1000 lab o'quvchilarni kerakli natijani olishizga sababchi bo'ldim</blockquote>
2⃣
<blockquote>Ustozlarimizni Ingliz tili darajasini 0 Dan sertifikat olish darajasigacha ko'tardim.</blockquote>

<b>Agar siz ham Bepul marafonda ishtirok etib maximal natijaga ega bo'lmoqchi bo'lsangiz:
SAT Elbek kanalga a'zo bo'ling

@satelbek</b>

Yetarli ballarga ega bo'ling yopiq kanal va guruhimiz a'zosiga aylaning.

<blockquote>⚠️ Joylar soni cheklangan, bunday imkoniyatni qo'ldan boy bermang 👇</blockquote>
{link}
{link}
{link}
""",
        'referral_link_error': "Taklif havolasini olishda xatolik yuz berdi.",
        
        # User stats messages        
        'user_stats_message': """
<b>📊 Sizning statistikangiz:</b>
<blockquote>👤 Foydalanuvchi: {user_mention}
🆔 Sizning ID: <code>{user_id}</code>{username_line}
✅ Tasdiqlangan takliflar: <b>{valid_referrals}</b>
⏳ Kutilayotgan takliflar: <b>{pending_referrals}</b></blockquote>
""",
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

        # New marathon messages
        'sat_marathon_info': """📢 Assalomu alaykum, SAT olmoqchi bolgan matematika ustozlarimiz hamda o'quvchilar!  

SAT imtixonini topshirmoqchisiz lekin natijalaringiz ozgarmayaptimi?

📌 Unda sizni 30 kunlik BEPUL Turbo Marafonimizga taklif qilaman!
<b>Men — Asatullayev Elbek:</b>
✅ 4 marta SAT Math 800/800 ball egasi
✅ Umumiy SAT natijam esa 1550/1600
✅  1000+ ustoz va o'quvchi SAT bo'yicha english nol darajadan tayyorlab 50 foiz ustamaga olib chiqqanman.
✅Barchani ingliz tili 0 dan natijagacha olib chiqmoqdaman
📊 Ushbu marafonda men sizlarga 30 kun davomida SAT Math bo'limidan mutloq tekin formatda jonli dars o'tib beraman. 
 Agar siz ham jonli darslarimizga qatnashib,ozingizda ozgarishni his qilib,Turbo Dekabr kursimizga qo'shilmoqchi bo'lsangiz. 
Marafon shartlarini bajaring va joyingizni oldindan band eting. 

Marafonda qoshilib, jonli darslarda qatnashish uchun "<b>‼️ Marafonda qatnashish sharti ‼️</b>" tugmasini bosing va kerakli ma'lumotni oling!""",

        'marathon_conditions': """🎯 <b>Bepul SAT Turbo Marafonida ishtirok eting!</b>
 1️⃣ Bot sizga shaxsiy taklif havolasini taqdim etadi. Siz ushbu havolani eng kamida 3 nafar SAT imtihoniga tayyorlanayotgan tanishlaringizga yuborishingiz kerak bo'ladi. Ular sizning havolangiz orqali botga kirsa, har biri uchun sizga 1 balldan beriladi.
2️⃣ Sizning ballaringiz 3 va undan ko'p bo'lsa, Ballarim bo'limi orqali siz uchun maxsus yopiq kanal va guruhga qo'shilish imkoniyatiga ega bo'lasiz.
🚫 Ballaringiz 3 dan kamayib ketsa, avtomatik tarzda guruh va kanaldan chetlatilasiz.
📌 Taklif havolangizni SAT ning matematika qismi bilan shug'ullanayotgan tanishlaringizga yuborishga harakat qiling!
✅ Tayyor bo'lsangiz, menyudan "<b>🔗 Taklif havolasi 🔗</b>" tugmasini bosing va do'stlaringizni taklif qiling!""",

        'new_referral_link_message': """❗️Qadirdonim yaxshiroq oqib deb, sizga ilindim😊
    
📌Ingliz tilim 0 darajada lekin SAT olaman deb niyat qilgan matematika ustozlar uchun bu ajoyib imkoniyat ✅

⚡️Oktabr oyining 1-sanasidan boshlab yopiq Bepul guruh tashkil qilinadi ✅

Darslarda faol qatnashib umumiy hisobda eng kamida 90 mln pul yutuq qolga kiriting🎁

•Bizda har kuni jonli darslar boladi

•Ingliz tilini 0 dan oshirishga maxsus topshiriqlarimiz

•Maximal natijaga erishishingiz uchun qoshimcha topshiriqlar

⚡️Yopiq guruhda vazifalarni toʻliq qilganlar orasidan 3 kishiga toʻliq xarajatlarini qoplagan holda 0 dan natijaga olib chiqamiz

❗️HOZIR VAQTI KEYIN KECH.

📌Bu guruhga ulanish bepul yani sizdan hech qanday toʻlov talab qilinmaydi🤝

•Hoziroq ulaning joylar kam👇

<blockquote>⚠️ Joylar soni cheklangan, bunday imkoniyatni qo'ldan boy bermang 👇</blockquote>
{link}""",

        'user_stats_new': """<b>📈 Ballarim</b>

sizning ballaringiz: <b>{current_points} ball</b>.

‼️ Siz taklif havolangiz orqali qo'shilgan odamlar kanallardan obunani bekor qilsa sizga shu odam uchun berilgan ball qaytarib olinadi!
✅ Hisobingizdagi ballar 3 balldan yuqori qiymatga ega bo'lgandan so'ng yopiq kanal va guruhimizga qo'shilishingiz mumkin bo'ladi.""",

        'prizes_info': """🏆 <b>Prizlar</b>

🏆 Marafonda sizni nafaqat bilim, balki KATTA imkoniyatlar ham kutmoqda!
📌 Marafon guruhida yuqori natija qayd etgan ustozlarimiz SAT Dekabr Turbo kursimizga chegirma asosida qabul qilinadi.
🎯 Qoshimchasiga, darslarni doimiy bajargan TOP-3 nafar ustozlarimiz yoki o'quvchilar uchun eng kamida 90 mln sum pul yutuq kutmoqda har biriga
<b>Biz 3 nafar odamning hammasiga:</b>
⚡️ SAT 111$ tolovni toliq qoplab beramiz
⚡️ Pullik maxsus kursimizda bepul oqitamiz
⚡️ Vazirlikka yuborish va boshqa barcha narsalarni ozimiz qilib beramiz
 <b>Sizdan harakat bizdan esa imkoniyatlar:</b>

SAT sertifikati orqali siz 3 yil davomida 50% ustama olasiz

Agar siz 5,000,000 oylik olsangiz

Bu 2,500,000*36 = 90,000,000 

<b>Barcha harajatlarni faol ustozlarimizga qoplab beramiz</b>""",
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
