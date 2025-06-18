from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.models import Database
from text.messages import get_text
from filters.user_filters import IsUserFilter
from keyboards.user_keyboards import get_main_user_keyboard
import logging

menu_router = Router()
menu_router.message.filter(IsUserFilter())

@menu_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, db: Database):
    """Handle /start command - registration and main menu"""
    await state.clear()
    
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name or ""
      # Check if user exists
    existing_user = await db.get_user(user_id)
    if existing_user:
        await message.answer(
            get_text('already_registered', 'uz'),
            reply_markup=get_main_user_keyboard()
        )
        return
      # Handle referral
    referrer = None
    referral_code = None
    args = message.text.split()
    logging.info(f"Start command args: {args}")
    if len(args) > 1:
        logging.info(f"Processing referral code: {args[1]}")
        referral_code = args[1]
        if len(referral_code) == 8:
            referrer = await db.get_user_by_referral_code(referral_code)
            if not referrer:
                await message.answer(get_text('invalid_referral', 'uz'))
                referral_code = None
            elif referrer['telegram_id'] == user_id:
                await message.answer(get_text('invalid_referral', 'uz'))
                referral_code = None
                referrer = None
        else:
            await message.answer(get_text('invalid_referral', 'uz'))
            referral_code = None    # Add user
    success, user_referral_code = await db.add_user(user_id, username, full_name)
    
    if referrer and referral_code:
        logging.info(f"Adding referral: referrer={referrer['telegram_id']}, referred={user_id}, code={referral_code}")
        success = await db.add_referral(referrer['telegram_id'], user_id, referral_code)
        logging.info(f"Referral added success: {success}")
        
        await message.answer(
            get_text('referral_welcome', 'uz', referrer=referrer['full_name']),
            reply_markup=get_main_user_keyboard()
        )
        
        # Check if both users are subscribed to validate referral
        bot = message.bot
        channel_ids = db.get_mandatory_channel_ids()
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
            notification_text = get_text(
                'referrer_new_user_subscribed', 
                'uz', 
                user_name=full_name or f"@{username}" or "Anonymous"
            )
            try:
                await bot.send_message(referrer['telegram_id'], notification_text)
            except Exception as e:
                logging.error(f"Failed to send notification to referrer {referrer['telegram_id']}: {e}")
        else:
            # Notify referrer that user joined but needs to subscribe
            notification_text = get_text(
                'referrer_new_user_pending', 
                'uz', 
                user_name=full_name or f"@{username}" or "Anonymous"
            )
            try:
                await bot.send_message(referrer['telegram_id'], notification_text)
            except Exception as e:
                logging.error(f"Failed to send notification to referrer {referrer['telegram_id']}: {e}")
    else:
        await message.answer(
            get_text('welcome', 'uz'),
            reply_markup=get_main_user_keyboard()
        )

@menu_router.message(F.text.in_([
    "📋 Qoidalar", "📋 Rules",
    "🎁 Sovg'a olish", "🎁 Get Reward", 
    "🔗 Mening taklif havolam", "🔗 My Referral Link",
    "📊 Mening statistikam", "📊 My Stats"
]))
async def menu_button_handler(message: Message, db: Database):
    """Handle main menu button presses"""
    
    if message.text in ["📋 Qoidalar", "📋 Rules"]:
        from .rules_handlers import show_rules
        await show_rules(message, db)
    elif message.text in ["🎁 Sovg'a olish", "🎁 Get Reward"]:
        from .reward_handlers import show_rewards
        await show_rewards(message, db)
    elif message.text in ["🔗 Mening taklif havolam", "🔗 My Referral Link"]:
        from .referral_handlers import show_referral_link
        await show_referral_link(message, db)
    elif message.text in ["📊 Mening statistikam", "📊 My Stats"]:
        from .stats_handlers import show_user_stats
        await show_user_stats(message, db)
