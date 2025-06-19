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
        # Check if user already accessed reward
        reward_text = get_text('reward_available', 'uz', 
                                 required_referrals=db.required_referrals,)
        if not await db.has_user_accessed_reward(user_id):
            # Mark as accessed
            await db.mark_reward_accessed(user_id)
        await message.answer(reward_text, reply_markup=get_reward_link_button(db.reward_link))
    else:
        # User doesn't have enough referrals yet
        remaining = db.required_referrals - valid_count
        reward_text = get_text('reward_not_available', 'uz',
                             required_referrals=db.required_referrals,
                             current_referrals=valid_count,
                             remaining_referrals=remaining)
    
        await message.answer(reward_text)
