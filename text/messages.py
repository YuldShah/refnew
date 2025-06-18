MESSAGES = {
    'uz': {
        'welcome': "Botga xush kelibsiz! 🎉",
        'referral_welcome': "Siz <b>{referrer}</b> tomonidan taklif qilindingiz! 🎉",
        'already_registered': "Siz allaqachon ro'yxatdan o'tgansiz!",
        'invalid_referral': "Noto'g'ri taklif havolasi!",
        'subscription_required': "Botdan foydalanish uchun barcha majburiy kanallarga obuna bo'ling:",
        'not_subscribed': "Siz hali ham barcha kanallarga obuna bo'lmagansiz!",
        'our_chats_folder': "Bizning kanallar papkasi 📁",
        'subscribe_button': "Obuna bo'lish ✅",
        'check_subscription': "Obunani tekshirish ✅",
        'subscription_confirmed': "✅ Tabriklaymiz! Siz barcha majburiy kanallarga obuna bo'ldingiz!",
        'referral_system': "Taklif tizimi 📊",
        'valid_referrals': "Tasdiqlangan takliflar: <b>{count}</b>",
        'pending_referrals': "Kutilayotgan takliflar: <b>{count}</b>",
        'your_referral_link': "Sizning taklif havolangiz:\n<code>{link}</code>",
        'admin_panel': "Admin panel 👨‍💼",
        'admin_top_referrers': "🏆 Top 10 referrerlar",
        'admin_user_lookup': "🔍 Foydalanuvchini qidirish",
        'admin_export_data': "📊 Ma'lumotlarni eksport qilish",
        'admin_stats': "📈 Statistika",
        'back_to_admin_menu': "⬅️ Admin menyuga qaytish",
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
        
        # Main menu buttons
        'rules_button': "📋 Qoidalar",
        'get_reward_button': "🎁 Sovg'a olish",
        'my_referral_link_button': "🔗 Mening taklif havolam",        'my_stats_button': "📊 Mening statistikam",
        'back_to_menu': "🔙 Bosh menyuga qaytish",        'refresh_stats': "🔄 Yangilash",
        'share_referral_link': "📤 Havolani ulashish",
        'stats_up_to_date': "📊 Statistika allaqachon yangi!",
        
        # Rules content (placeholder)
        'rules_content': """📋 <b>Bot qoidalari</b>

🔹 Botdan foydalanish uchun barcha majburiy kanallarga obuna bo'ling
🔹 Taklif havolangizni do'stlaringiz bilan ulashing
🔹 Har bir tasdiqlangan taklif uchun mukofot oling
🔹 Spam va noto'g'ri harakatlar taqiqlanadi

Bu yerda qoidalar to'liq yoziladi...""",
        
        # Reward content (placeholder)
        'reward_content': """🎁 <b>Mukofotlar</b>

💰 Har bir tasdiqlangan taklif uchun: 1000 so'm
🎯 5 taklif uchun: 10,000 so'm bonus
🏆 10 taklif uchun: 25,000 so'm bonus

Bu yerda mukofotlar tizimi to'liq yoziladi...""",
        
        # Referral link messages
        'referral_link_message': """🔗 <b>Sizning taklif havolangiz:</b>

<code>{link}</code>

Bu havolani do'stlaringiz bilan ulashing va mukofot oling! 💰""",
        'referral_link_error': "Taklif havolasini olishda xatolik yuz berdi.",
        
        # User stats messages        
        'user_stats_message': """📊 <b>Sizning statistikangiz:</b>

👥 Jami takliflar: <b>{total_referrals}</b>
✅ Tasdiqlangan takliflar: <b>{valid_referrals}</b>
⏳ Kutilayotgan takliflar: <b>{pending_referrals}</b>

Davom eting va ko'proq mukofot oling! 🎯""",
        'referrals_validated': """🎉 <b>Yangilik!</b> Do'stlaringizdan {count} ta yangi taklif tasdiqlandi!""",
        
        # Referrer notification messages
        'referrer_new_user_subscribed': """🎉 <b>New user!</b>

👤 {user_name} joined the bot through your referral and subscribed to all mandatory channels!

✅ This referral has been added to your confirmed referrals list.""",
        
        'referrer_new_user_pending': """🔔 <b>New user!</b>

👤 {user_name} joined the bot through your referral.

⏳ Currently waiting for them to subscribe to mandatory channels. The referral will be confirmed once they subscribe.""",
        
        'referrer_user_subscribed': """🎉 <b>Referral confirmed!</b>

👤 {user_name} has subscribed to mandatory channels!

✅ This referral is now in your confirmed referrals list.""",
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
        'admin_export_data': "📊 Export user data",
        'admin_stats': "📈 Statistics",
        'back_to_admin_menu': "⬅️ Back to admin menu",
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
        'my_referral_link_button': "🔗 My Referral Link",        'my_stats_button': "📊 My Stats",
        'back_to_menu': "🔙 Back to Menu",        'refresh_stats': "🔄 Refresh",
        'share_referral_link': "📤 Share Link",
        'stats_up_to_date': "📊 Stats are already up to date!",
        
        # Rules content (placeholder)
        'rules_content': """📋 <b>Bot Rules</b>

🔹 Subscribe to all mandatory channels to use the bot
🔹 Share your referral link with friends
🔹 Get rewards for each confirmed referral
🔹 Spam and inappropriate behavior is prohibited

Complete rules will be written here...""",
        
        # Reward content (placeholder)
        'reward_content': """🎁 <b>Rewards</b>

💰 For each confirmed referral: 1000 som
🎯 For 5 referrals: 10,000 som bonus
🏆 For 10 referrals: 25,000 som bonus

Complete reward system will be described here...""",
        
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

👤 {user_name} sizning taklifingiz orqali botga qo'shildi va barcha majburiy kanallarga obuna bo'ldi!

✅ Bu taklif tasdiqlangan takliflar ro'yxatiga qo'shildi.""",
        
        'referrer_new_user_pending': """🔔 <b>Yangi foydalanuvchi!</b>

👤 {user_name} sizning taklifingiz orqali botga qo'shildi.

⏳ Hozircha majburiy kanallarga obuna bo'lishi kutilmoqda. Obuna bo'lgandan so'ng taklif tasdiqlanadi.""",
        
        'referrer_user_subscribed': """🎉 <b>Taklif tasdiqlandi!</b>

👤 {user_name} majburiy kanallarga obuna bo'ldi!

✅ Bu taklif endi tasdiqlangan takliflar ro'yxatida.""",
    }
}

def get_text(key: str, lang: str = 'uz', **kwargs) -> str:
    text = MESSAGES.get(lang, MESSAGES['uz']).get(key, key)
    return text.format(**kwargs) if kwargs else text

async def get_user_text(key: str, user_id: int, db, **kwargs) -> str:
    lang = await db.get_user_language(user_id)
    return get_text(key, lang, **kwargs)
