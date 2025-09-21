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
        return    # Add user
    success, user_referral_code = await db.add_user(user_id, username, full_name)
    
    if referrer and referral_code:
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
          # Check if both users are subscribed to validate referral
        bot = message.bot
        channel_ids = await db.get_mandatory_channel_ids()
        logging.info(f"Checking subscription for channels: {channel_ids}")
        
        both_subscribed = True
        for channel_id in channel_ids:
            try:
                referrer_member = await bot.get_chat_member(channel_id, referrer['telegram_id'])
                user_member = await bot.get_chat_member(channel_id, user_id)
                
                referrer_status = referrer_member.status
                user_status = user_member.status
                
                logging.info(f"Channel {channel_id} - Referrer status: {referrer_status}, User status: {user_status}")
                  # In aiogram 3.x, the valid statuses are "member", "administrator", "creator"
                if (referrer_status not in ['member', 'administrator', 'creator'] or 
                    user_status not in ['member', 'administrator', 'creator']):
                    both_subscribed = False
                    logging.info(f"Not subscribed: referrer_status={referrer_status}, user_status={user_status}")
                    break
            except Exception as e:
                both_subscribed = False
                logging.error(f"Subscription check error: {str(e)}")
                break
        
        if both_subscribed:
            logging.info(f"Validating referral: referrer={referrer['telegram_id']}, referred={user_id}")
            await db.validate_referral(referrer['telegram_id'], user_id)
              # Notify referrer that user joined and is already subscribed
            # Create user mention (prefer mention_html, fallback to tg deep link)
            user_mention = f'<a href="tg://user?id={user_id}">{full_name or f"@{username}" or "User"}</a>'

            notification_text = get_text(
                'referrer_new_user_subscribed',
                'uz',
                user_name=user_mention
            )
            try:
                await bot.send_message(referrer['telegram_id'], notification_text)
            except Exception as e:
                logging.error(f"Failed to send notification to referrer {referrer['telegram_id']}: {e}")
        else:
            # Notify referrer that user joined but needs to subscribe
            # Create user mention (prefer mention_html, fallback to tg deep link)
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
    "🔗Taklif havolasi🔗",
    "Prizlar🏆", 
    "Ballarim📈",
    "🔝SAT marafon haqida🔝",
    "‼️ Marafonda qatnashish sharti ‼️"
]))
async def new_marathon_buttons_handler(message: Message, db: Database):
    """Handle new marathon button presses"""
    
    # Check if user exists before allowing access to any menu features
    user = await db.get_user(message.from_user.id)
    if not user:
        # Get user's language preference (fallback to telegram language or default 'uz')
        user_lang = 'uz'
        await message.answer(
            get_text('register_first', user_lang)
        )
        return
    
    if message.text == "🔗Taklif havolasi🔗":
        from .referral_handlers import show_new_referral_link
        await show_new_referral_link(message, db)
    elif message.text == "Prizlar🏆":
        await message.answer_photo(photo="AgACAgIAAxkBAANKaMz4Y9AdZDJBTlm4vIAIgkFWpTwAAoX3MRsM6GlKqL91bcYgiYkBAAMCAAN5AAM2BA", caption=get_text('prizes_info', 'uz'))
    elif message.text == "Ballarim📈":
        from .stats_handlers import show_user_points
        await show_user_points(message, db)
    elif message.text == "🔝SAT marafon haqida🔝":
        await message.answer(get_text('sat_marathon_info', 'uz'))
    elif message.text == "‼️ Marafonda qatnashish sharti ‼️":
        await message.answer(get_text('marathon_conditions', 'uz'))

@menu_router.inline_query()
async def handle_inline_query(inline_query: InlineQuery, db: Database):
    """Handle inline queries for referral links"""
    from .referral_handlers import handle_inline_query
    await handle_inline_query(inline_query, db)
