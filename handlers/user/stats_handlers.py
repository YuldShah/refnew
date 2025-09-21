from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from database.models import Database
from text.messages import get_text
from keyboards.user_keyboards import get_stats_keyboard, get_reward_link_button
from services.referral_service import ReferralService

async def show_user_stats(message: Message, db: Database):
    """Display user's referral statistics and overall bot stats"""
    referral_service = ReferralService(db)
      # Check and validate any pending referrals
    validation_result = await referral_service.check_and_validate_pending_referrals(
        message.from_user.id, message.bot
    )
    
    # Check for reward eligibility and notify if needed
    reward_check = await referral_service.check_and_notify_reward_eligibility(
        message.from_user.id, message.bot
    )
    
    # Get updated user stats after validation
    user_stats = await referral_service.get_referral_stats(message.from_user.id)
      # Add user info to stats
    user_stats['user_id'] = message.from_user.id
    user_stats['user_mention'] = message.from_user.mention_html()

    # Add username line only if user has a username
    if message.from_user.username:
        user_stats['username_line'] = f"\n👤 Username: <b>@{message.from_user.username}</b>"
    else:
        user_stats['username_line'] = ""

    # Create user stats text (only user's personal stats)
    text = get_text('user_stats_message', 'uz', **user_stats)
    
    await message.answer(
        text,
        reply_markup=get_stats_keyboard()
    )

async def show_user_points(message: Message, db: Database):
    """Display user's points for the marathon"""
    referral_service = ReferralService(db)
    user_id = message.from_user.id
    
    # Check and validate any pending referrals
    validation_result = await referral_service.check_and_validate_pending_referrals(
        user_id, message.bot
    )
    
    # Get updated user stats after validation
    user_stats = await referral_service.get_referral_stats(user_id)
    current_points = user_stats.get('valid_referrals', 0)
    
    # Create points text
    text = get_text('user_stats_new', 'uz', current_points=current_points)
    
    if current_points >= 3:
        # User has enough points for reward
        text = get_text('user_stats_for_rewarding', 'uz', current_points=current_points)
        
        # Check if user has already accessed reward
        if await db.has_user_accessed_reward(user_id):
            # Get existing reward data from database
            reward_data = await db.get_user_reward(user_id)
            if reward_data and 'links' in reward_data:
                # Use existing links
                links = reward_data['links']
                await message.answer(text, reply_markup=get_reward_link_button(links))
            else:
                # Fallback: regenerate links if data is corrupted
                links = await _generate_invite_links(message, user_id)
                await _save_reward_data(db, user_id, links)
                await message.answer(text, reply_markup=get_reward_link_button(links))
        else:
            # First time accessing reward - generate new links
            links = await _generate_invite_links(message, user_id)
            await _save_reward_data(db, user_id, links)
            await message.answer(text, reply_markup=get_reward_link_button(links))
    else:
        # User doesn't have enough points yet
        await message.answer(text)

async def _generate_invite_links(message: Message, user_id: int) -> list:
    """Generate invite links for reward channels"""
    # Bepul darslar guruhi
    link1_obj = await message.bot.create_chat_invite_link(
        chat_id=-1003087849002,
        name=f"Join link for {user_id}",
        member_limit=1
    )

    # Bepul darslar kanali
    link2_obj = await message.bot.create_chat_invite_link(
        chat_id=-1002914914573,
        name=f"Join link for {user_id}",
        member_limit=1
    )

    # Muhokama guruhi
    link3_obj = await message.bot.create_chat_invite_link(
        chat_id=-1003077395393,
        name=f"Join link for {user_id}",
        member_limit=1
    )

    # Extract the actual invite link URLs from ChatInviteLink objects
    return [link1_obj.invite_link, link2_obj.invite_link, link3_obj.invite_link]

async def _save_reward_data(db: Database, user_id: int, links: list):
    """Save reward data to database"""
    reward_data = {
        'links': links
    }
    await db.save_user_reward(user_id, reward_data)


async def refresh_user_stats(callback: CallbackQuery, db: Database):
    """Handle refresh stats button press"""
    await callback.answer("🔄 Refreshing stats...")
    
    referral_service = ReferralService(db)
      # Check and validate any pending referrals
    validation_result = await referral_service.check_and_validate_pending_referrals(
        callback.from_user.id, callback.bot
    )
    
    # Check for reward eligibility and notify if needed
    reward_check = await referral_service.check_and_notify_reward_eligibility(
        callback.from_user.id, callback.bot
    )
    
    # Get updated user stats after validation
    user_stats = await referral_service.get_referral_stats(callback.from_user.id)
      # Add user info to stats
    user_stats['user_id'] = callback.from_user.id
    user_stats['user_mention'] = callback.from_user.mention_html()

    # Add username line only if user has a username
    if callback.from_user.username:
        user_stats['username_line'] = f"\n👤 Username: <b>@{callback.from_user.username}</b>"
    else:
        user_stats['username_line'] = ""

    # Create user stats text (only user's personal stats)
    text = get_text('user_stats_message', 'uz', **user_stats)
    
    # Add validation result if any referrals were validated
    if validation_result["validated"] > 0:
        validation_text = get_text(
            'referrals_validated', 
            'uz', 
            count=validation_result["validated"]
        )
        text += f"\n{validation_text}"
    else:
        # Add refresh timestamp to make message different
        from datetime import datetime
        refresh_time = datetime.now().strftime("%H:%M")
        refresh_text = f"🔄 Oxirgi yangilanish: {refresh_time}"
        text += f"\n{refresh_text}"
    
    # Try to edit the message, but handle the case where content is the same
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_stats_keyboard()
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            # If message content is the same, just show a notification
            await callback.answer(get_text('stats_up_to_date', 'uz'), show_alert=True)
        else:            # Re-raise other TelegramBadRequest exceptions
            raise e
