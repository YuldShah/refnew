MESSAGES = {
    'uz': {
        'welcome': """👋 Assalomu alaykum, <b>{link_to_user}</b>!

<i>📖 3 Marta SAT matematika qismidan maximal 800/800 ball olgan Elbek ustoz o'tayotgan Bepul darslarimizga xush kelibsiz!</i>

Bizning bepul darslarda qatnashish uchun siz quyidagi shartlarni bajarishingiz kerak:
<blockquote>1️⃣ Barcha kanallarimizga a'zo bo'ling
2️⃣ 3 ta SAT matematika qismidan eng yuqori natijani olaman va 50% ustamani olishni chin dildan niyat qilgan tanishlarni botimizga taklif qiling va ular ham bizning barcha kanallarimizga a'zo bo'lib eng muhim bilimlarni olishsin)</blockquote>

Qoshimcha ma'lumotlar uchun quyidagi menyudan foydalansangiz bo'ladi.""",
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
        'rules_button': "📋 Qoidalar",
        'get_reward_button': "🚀 Kirish huquqini olish",
        'my_referral_link_button': "🔗 Mening taklif havolam",        'my_stats_button': "📊 Mening statistikam",
        'share_referral_link': "🔗 Referral havolani ulashish",
        'back_to_menu': "🔙 Bosh menyuga qaytish",        'refresh_stats': "🔄 Yangilash",
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

        'referrer_new_user_already_in_channels': """⚠️ <b>Taklif hisoblanmadi</b>

👤 {user_name} sizning taklifingiz orqali botga ro'yxatdan o'tdi.

🚫 Taklif qilingan foydalanuvchi yangi a'zo emas""",
        
        'referrer_user_subscribed': """🎉 <b>Taklif tasdiqlandi!</b>

👤 {user_name} bizning kanallarga obuna bo'ldi!

✅ Bu taklif endi tasdiqlangan takliflar ro'yxatida.""",
    },
    'en': {
        'welcome': "Welcome to the bot! 🎉",
        'referral_welcome': "You were invited by <b>{referrer}</b>! 🎉",

        'referrer_new_user_already_in_channels': """⚠️ <b>Referral not counted</b>

👤 {user_name} joined the bot through your referral link.

🚫 That user was already in at least one mandatory chat before registering, so this referral does not count.""",
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
