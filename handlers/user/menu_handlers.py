from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineQuery
from aiogram.fsm.context import FSMContext
from database.models import Database
from text.messages import get_text
from filters.user_filters import IsUserFilter
from keyboards.user_keyboards import get_main_user_keyboard
import logging

menu_router = Router()
menu_router.message.filter(IsUserFilter())

@menu_router.message(F.text == "🏘 Main menu")
@menu_router.message(F.text == "🏘 Bosh menyu")
@menu_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, db: Database):
    """Handle /start command - registration and main menu"""
    await state.clear()
    
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name or ""

    # Handle start parameters first (before checking existing user)
    referrer = None
    referral_code = None
    args = message.text.split()
    logging.info(f"Start command args: {args}")
    if len(args) > 1:
        param = args[1]
        logging.info(f"Processing start parameter: {param}")

        # Handle subscription required parameter
        if param == "sub":
            # Show subscription required message for any user (new or existing)
            from middleware.subscription import SubscriptionMiddleware
            middleware = SubscriptionMiddleware(db)
            keyboard = await middleware.create_subscription_keyboard()
            await message.answer(
                get_text('subscription_required', 'uz'),
                reply_markup=keyboard
            )
            return

        # Handle access denied parameter
        if param == "access_denied":
            # Show access denied message
            text = "🚫 <b>Kirish taqiqlangan</b>\n\n"
            text += "Sizga bu botdan foydalanish taqiqlangan."
            await message.answer(text)
            return

        # Handle referral code (8 characters) - only for new users
        if len(param) == 8:
            referral_code = param
            referrer = await db.get_user_by_referral_code(referral_code)
            if not referrer:
                await message.answer(get_text('invalid_referral', 'uz'))
                referral_code = None
            elif referrer['telegram_id'] == user_id:
                await message.answer(get_text('invalid_referral', 'uz'))
                referral_code = None
                referrer = None
        else:
            # Invalid parameter
            await message.answer(get_text('invalid_referral', 'uz'))
            referral_code = None

    # Check if user exists (after handling special parameters)
    existing_user = await db.get_user(user_id)
    if existing_user and len(args) > 1:
        await message.answer(
            get_text('welcome', 'uz', link_to_user=message.from_user.mention_html()),
            reply_markup=get_main_user_keyboard()
        )
        await message.answer(
            get_text('already_registered', 'uz'),
        )
        return
    
    # Add user
    success, user_referral_code = await db.add_user(user_id, username, full_name)
    
    if referrer and referral_code:
        bot = message.bot
        channel_ids = await db.get_mandatory_channel_ids()
        
        # Check if new user was ALREADY subscribed to ALL channels BEFORE clicking referral link
        # If they were already subscribed to all, they weren't brought by the referrer
        user_already_subscribed_to_one = False
        if channel_ids:
            for channel_id in channel_ids:
                try:
                    user_member = await bot.get_chat_member(channel_id, user_id)
                    if user_member.status in ['member', 'administrator', 'creator']:
                        user_already_subscribed_to_one = True
                        break
                except Exception as e:
                    print("Error while checking the subscription")
                    break
        else:
            # No mandatory channels configured
            user_already_subscribed_to_one = False
        
        if user_already_subscribed_to_one:
            # User was already subscribed to at least one channel - don't count as referral
            logging.info(f"User {user_id} was already subscribed to at least one channel - not counting referral from {referrer['telegram_id']}")
            await bot.send_message(referrer['telegram_id'], "Siz taklif qilgan foydalunchi oldindan kanallarimizda mavjud edi. Bu referral hisobga olinmaydi.")
            await message.answer(
                get_text('welcome', 'uz', link_to_user=message.from_user.mention_html()),
                reply_markup=get_main_user_keyboard()
            )
            # Don't show referral welcome or create referral record
        else:
            # User is NOT subscribed to at least one channel - valid referral candidate
            logging.info(f"Adding referral: referrer={referrer['telegram_id']}, referred={user_id}, code={referral_code}")
            success = await db.add_referral(referrer['telegram_id'], user_id, referral_code)
            logging.info(f"Referral added success: {success}")
            
            await message.answer(
                get_text('welcome', 'uz', link_to_user=message.from_user.mention_html()),
                reply_markup=get_main_user_keyboard()
            )

            # Create referrer mention (prefer mention_html, fallback to tg deep link)
            referrer_mention = f'<a href="tg://user?id={referrer["telegram_id"]}">{referrer["full_name"] or "User"}</a>'

            await message.answer(
                get_text('referral_welcome', 'uz', referrer=referrer_mention),
            )
            
            # Check if referrer is also subscribed to validate referral immediately
            logging.info(f"Checking subscription for channels: {channel_ids}")
            
            referrer_subscribed = True
            for channel_id in channel_ids:
                try:
                    referrer_member = await bot.get_chat_member(channel_id, referrer['telegram_id'])
                    if referrer_member.status not in ['member', 'administrator', 'creator']:
                        referrer_subscribed = False
                        break
                except Exception as e:
                    referrer_subscribed = False
                    logging.error(f"Subscription check error: {str(e)}")
                    break
            
            # Now check if new user subscribed (they weren't before, but middleware may have prompted them)
            # For now, the referral stays pending until user subscribes via check_subscription callback
            
            # Notify referrer about new pending referral
            user_mention = f'<a href="tg://user?id={user_id}">{full_name or f"@{username}" or "User"}</a>'

            notification_text = get_text(
                'referrer_new_user_pending',
                'uz',
                user_name=user_mention
            )
            try:
                await bot.send_message(referrer['telegram_id'], notification_text)
            except Exception as e:
                logging.error(f"Failed to send notification to referrer {referrer['telegram_id']}: {e}")
    else:
        await message.answer(
            get_text('welcome', 'uz', link_to_user=message.from_user.mention_html()),
            reply_markup=get_main_user_keyboard()
        )

@menu_router.message(F.text.in_([
    "📋 SAT marafon haqida 📋",
    "‼️ Marafonda qatnashish sharti ‼️",
    "🎁 Sovrinlar ⭐️",
    "🔗Taklif havolasi🔗",
    "👇SAT imtixoni beradigan imkoniyatlar👇",
    "📊Ballarim📊"
]))
async def menu_button_handler(message: Message, db: Database):
    """Handle main menu button presses"""
    
    # Check if user exists before allowing access to any menu features
    user = await db.get_user(message.from_user.id)
    if not user:
        # Get user's language preference (fallback to telegram language or default 'uz')
        user_lang = 'uz'
        await message.answer(
            get_text('register_first', user_lang)
        )
        return
    
    if message.text == "‼️ Marafonda qatnashish sharti ‼️":
        from .rules_handlers import show_rules
        await show_rules(message, db)
    elif message.text == "📊Ballarim📊":
        from .reward_handlers import show_rewards
        await show_rewards(message, db)
    elif message.text == "🔗Taklif havolasi🔗":
        from .referral_handlers import show_referral_link
        await show_referral_link(message, db)
    elif message.text == "📋 SAT marafon haqida 📋":
        from .stats_handlers import show_about_olympiad
        await show_about_olympiad(message, db)
    elif message.text == "🎁 Sovrinlar ⭐️":
        from .stats_handlers import show_rewards_info
        await show_rewards_info(message, db)
    elif message.text == "👇SAT imtixoni beradigan imkoniyatlar👇":
        from .stats_handlers import show_sat_opportunities
        await show_sat_opportunities(message, db)

@menu_router.inline_query()
async def handle_inline_query(inline_query: InlineQuery, db: Database):
    """Handle inline queries for referral links"""
    from .referral_handlers import handle_inline_query
    await handle_inline_query(inline_query, db)
