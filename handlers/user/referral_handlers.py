from aiogram.types import Message, InlineQuery, InlineQueryResultVideo
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
    
    await message.answer_video(
        video="BAACAgIAAxkBAAIR4WhUZZTFkl_JvLlAkgod_CQFMljrAAIqdAACA1k4SRSFKq0mGiTUNgQ",
        caption=text,
        reply_markup=keyboard
    )

async def handle_inline_query(inline_query: InlineQuery, db: Database):
    """Handle inline queries for sharing referral videos"""
    import logging
    logging.info(f"handle_inline_query called for user {inline_query.from_user.id}")
    
    user_id = inline_query.from_user.id
    
    # Get user's referral code
    user = await db.get_user(user_id)
    if not user:
        logging.warning(f"User {user_id} not found in database")
        await inline_query.answer([])
        return
    
    # Get bot username
    bot_info = await inline_query.bot.get_me()
    bot_username = bot_info.username
    
    # Create referral link
    referral_link = f"https://t.me/{bot_username}?start={user['referral_code']}"
    
    # Create video result
    video_result = InlineQueryResultVideo(
        id="referral_video",
        video_url="BAACAgIAAxkBAAIR4WhUZZTFkl_JvLlAkgod_CQFMljrAAIqdAACA1k4SRSFKq0mGiTUNgQ",
        mime_type="video/mp4",  # Optional thumbnail
        title="Referral havolasi",
        thumbnail_url="https://i.postimg.cc/5yCpybYn/uplimg.jpg",
        description="Referral havolangizni ulashing",
        caption=get_text('referral_link_message', 'uz', link=referral_link)
    )
    
    await inline_query.answer([video_result], cache_time=0)

async def handle_inline_query_for_not_subbed(inline_query: InlineQuery, db: Database):
    """Handle inline queries for users who are not subscribed"""
    await inline_query.answer(
        [],
        cache_time=0,
        switch_pm_text="Avval bizning kanallarga obuna bo'ling!",
        switch_pm_parameter="sub"
    )
