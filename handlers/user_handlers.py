from aiogram import Router
from handlers.user.menu_handlers import menu_router
from handlers.user.stats_handlers import refresh_user_stats
from keyboards.user_keyboards import get_main_user_keyboard
from text.messages import get_text
from aiogram.types import CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
import logging

# Create main user router that includes all sub-routers
user_router = Router()
# Filter to only handle private chats (except inline queries which don't have chat type)
user_router.message.filter(F.chat.type == "private")
user_router.callback_query.filter(F.message.chat.type == "private")
user_router.include_router(menu_router)

@user_router.callback_query(F.data == 'back_to_menu')
async def back_to_menu_handler(callback: CallbackQuery, db):
    """Handle back to menu callback"""
    await callback.message.delete()
    await callback.message.answer(
        get_text('welcome', 'uz'),
        reply_markup=get_main_user_keyboard()
    )
    await callback.answer()

@user_router.callback_query(F.data == 'check_subscription')
async def check_subscription_handler(callback: CallbackQuery, db):
    """Handle subscription check and validate referrals if user is now subscribed"""
    user_id = callback.from_user.id
    bot = callback.bot
      # Check subscription status
    channel_ids = await db.get_mandatory_channel_ids()
    all_subscribed = True
    
    for channel_id in channel_ids:
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                all_subscribed = False
                break
        except Exception as e:
            all_subscribed = False
            break
    
    if all_subscribed:
        # Validate any pending referrals for this user
        validation_result = await db.validate_user_referrals(user_id)
        
        # Notify referrers about newly validated referrals
        if validation_result["validated"] > 0:
            # Get who referred this user and notify them
            async with db.pool.acquire() as conn:
                referrers = await conn.fetch('''
                    SELECT u.telegram_id, u.full_name, u.username 
                    FROM referrals r 
                    JOIN users u ON r.referrer_id = u.id 
                    WHERE r.referred_id = (SELECT id FROM users WHERE telegram_id = $1) 
                    AND r.valid = TRUE
                ''', user_id)
                
                for referrer in referrers:
                    # Create user mention (prefer mention_html, fallback to tg deep link)
                    user_mention = f'<a href="tg://user?id={callback.from_user.id}">{callback.from_user.full_name or f"@{callback.from_user.username}" or "User"}</a>'

                    notification_text = get_text(
                        'referrer_user_subscribed',
                        'uz',
                        user_name=user_mention
                    )
                    try:
                        await callback.bot.send_message(referrer['telegram_id'], notification_text)
                    except Exception as e:
                        logging.error(f"Failed to send notification to referrer {referrer['telegram_id']}: {e}")
        
        # Show success message
        success_text = get_text('subscription_confirmed', 'uz')
        
        await callback.message.edit_text(success_text)
        
        # Send main menu in a new message
        await callback.message.answer(
            get_text('welcome', 'uz', link_to_user=callback.from_user.mention_html()),
            reply_markup=get_main_user_keyboard()
        )
    else:
        # User is still not subscribed - show subscription required message again
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=get_text('our_chats_folder', 'uz'),
                url="REPLACED"
            )],
            [InlineKeyboardButton(
                text=get_text('check_subscription', 'uz'),
                callback_data='check_subscription'
            )]
        ])
        
        try:
            await callback.message.edit_text(
                get_text('not_subscribed', 'uz'),
                reply_markup=keyboard
            )
        except Exception as e:
            logging.error(f"Failed to edit message")
        finally:
            await callback.answer(get_text('not_subscribed', 'uz'), show_alert=True)
    
    await callback.answer()

@user_router.callback_query(F.data == 'refresh_stats')
async def refresh_stats_handler(callback: CallbackQuery, db):
    """Handle refresh stats callback"""
    await refresh_user_stats(callback, db)
