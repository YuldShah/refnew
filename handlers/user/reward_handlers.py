from aiogram.types import Message
from database.models import Database
from text.messages import get_text
from services.referral_service import ReferralService
from keyboards.user_keyboards import get_reward_link_button

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
            if reward_data and 'links' in reward_data:
                # Use existing links
                links = reward_data['links']
                await message.answer(reward_text, reply_markup=get_reward_link_button(links), protect_content=True)
            else:
                # Fallback: regenerate links if data is corrupted
                links = await _generate_invite_links(message, user_id)
                await _save_reward_data(db, user_id, links)
                await message.answer(reward_text, reply_markup=get_reward_link_button(links), protect_content=True)
        else:
            # First time accessing reward - generate new links
            links = await _generate_invite_links(message, user_id)
            await _save_reward_data(db, user_id, links)
            await message.answer(reward_text, reply_markup=get_reward_link_button(links), protect_content=True)
    else:
        # User doesn't have enough referrals yet
        remaining = db.required_referrals - valid_count
        reward_text = get_text('reward_not_available', 'uz',
                             required_referrals=db.required_referrals,
                             current_referrals=valid_count,
                             remaining_referrals=remaining)

        await message.answer(reward_text)

async def _generate_invite_links(message: Message, user_id: int) -> list:
    """Generate invite links for reward channels"""
    # Bepul darslar guruhi
    link1_obj = await message.bot.create_chat_invite_link(
        chat_id=-1002746646141,
        name=f"Join link for {user_id}",
        member_limit=1
    )

    # Bepul darslar kanali
    link2_obj = await message.bot.create_chat_invite_link(
        chat_id=-1002510444446,
        name=f"Join link for {user_id}",
        member_limit=1
    )

    # Muhokama guruhi
    link3_obj = await message.bot.create_chat_invite_link(
        chat_id=-1002861603252,
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
