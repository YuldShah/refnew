from aiogram.types import Message
from database.models import Database
from text.messages import get_text
from keyboards.user_keyboards import get_referral_share_keyboard
from services.referral_service import ReferralService

async def show_referral_link(message: Message, db: Database):
    """Display user's referral link"""
    referral_service = ReferralService(db)
    
    # Get bot username dynamically
    bot = message.bot
    bot_info = await bot.get_me()
    bot_username = bot_info.username
    
    referral_link = await referral_service.get_user_referral_link(message.from_user.id, bot_username)
    
    if referral_link:
        text = get_text('referral_link_message', 'uz', link=referral_link)
        keyboard = get_referral_share_keyboard(referral_link)
    else:
        text = get_text('referral_link_error', 'uz')
        keyboard = None
    
    await message.answer(
        text,
        reply_markup=keyboard
    )
