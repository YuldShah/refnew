from aiogram.types import Message
from database.models import Database
from text.messages import get_text
from services.referral_service import ReferralService
from keyboards.user_keyboards import get_reward_link_button
from config.loader import get_reward_channels

async def show_rewards(message: Message, db: Database):
    """Display available rewards to user"""
    user_id = message.from_user.id
    referral_service = ReferralService(db)

    # Get user's valid referrals count
    valid_referrals = await referral_service.get_referral_stats(user_id)
    valid_count = valid_referrals.get('valid_referrals', 0)

    # Check if user has enough referrals for reward
    if valid_count >= db.required_referrals:
        reward_text = get_text('reward_available', 'uz',
                                 required_referrals=db.required_referrals,)

        # Check if user has already accessed reward
        if await db.has_user_accessed_reward(user_id):
            # Get existing reward data from database
            reward_data = await db.get_user_reward(user_id)
            if reward_data and 'invite_data' in reward_data:
                # Use existing invite data
                invite_data = reward_data['invite_data']
                await message.answer(reward_text, reply_markup=get_reward_link_button(invite_data))
            else:
                # Fallback: regenerate links if data is corrupted or old format
                invite_data = await _generate_invite_links(message, user_id)
                await _save_reward_data(db, user_id, invite_data)
                await message.answer(reward_text, reply_markup=get_reward_link_button(invite_data))
        else:
            # First time accessing reward - generate new links
            invite_data = await _generate_invite_links(message, user_id)
            await _save_reward_data(db, user_id, invite_data)
            await message.answer(reward_text, reply_markup=get_reward_link_button(invite_data))
    else:
        # User doesn't have enough referrals yet
        remaining = db.required_referrals - valid_count
        reward_text = get_text('reward_not_available', 'uz',
                             required_referrals=db.required_referrals,
                             current_referrals=valid_count,
                             remaining_referrals=remaining)

        await message.answer(reward_text)

async def _generate_invite_links(message: Message, user_id: int) -> list:
    """Generate invite links for reward channels (loaded dynamically from config)"""
    channels = get_reward_channels()
    invite_data = []

    for channel in channels:
        try:
            link_obj = await message.bot.create_chat_invite_link(
                chat_id=channel['chat_id'],
                name=f"{channel['name']} - User {user_id}",
                member_limit=1
            )
            invite_data.append({
                'name': channel['name'],
                'link': link_obj.invite_link
            })
        except Exception as e:
            print(f"Error creating invite link for {channel['name']}: {e}")
            # Continue with other channels even if one fails
            continue

    return invite_data

async def _save_reward_data(db: Database, user_id: int, invite_data: list):
    """Save reward data to database"""
    reward_data = {
        'invite_data': invite_data
    }
    await db.save_user_reward(user_id, reward_data)
