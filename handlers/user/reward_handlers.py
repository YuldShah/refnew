from aiogram.types import Message
from database.models import Database
from text.messages import get_text
from services.referral_service import ReferralService
from keyboards.user_keyboards import get_reward_link_button

# Olympiad channel ID
OLYMPIAD_CHANNEL_ID = -1003676076162

async def show_rewards(message: Message, db: Database):
    """Display user's points and reward access if eligible"""
    user_id = message.from_user.id
    referral_service = ReferralService(db)

    # Get user's valid referrals count (points)
    valid_referrals = await referral_service.get_referral_stats(user_id)
    valid_count = valid_referrals.get('valid_referrals', 0)
    user_mention = message.from_user.full_name or message.from_user.username or "Foydalanuvchi"

    # Check if user has enough referrals (3 or more points)
    base_text = f"""<b>📈 Sizning ballaringiz: {valid_count} ball.</b>
<blockquote>‼️ Siz taklif havolangiz orqali qo'shilgan odam kanallardan obunani bekor qilsa sizga shu odam uchun berilgan ball qaytarib olinadi!</blockquote>
<b>✅ Hisobingizdagi ballar 3 balldan yuqori qiymatga ega bo‘lgandan so‘ng yopiq kanal va guruhimizga qo‘shilishingiz mumkin bo‘ladi.</b>"""

    if valid_count >= db.required_referrals:
        # User has enough points - show reward with channel link
        reward_text = base_text + "\n\n<b>✅ Tabriklaymiz! Siz yopiq kanal va guruhimizga qo'shilishingiz mumkin!</b>"

        # Check if user has already accessed reward
        if await db.has_user_accessed_reward(user_id):
            # Get existing reward data from database
            reward_data = await db.get_user_reward(user_id)
            if reward_data and 'links' in reward_data:
                # Use existing link
                link = reward_data['links'][0] if isinstance(reward_data['links'], list) else reward_data['links']
                await message.answer(reward_text, reply_markup=get_reward_link_button(link), protect_content=True)
            else:
                # Fallback: regenerate link if data is corrupted
                link = await _generate_invite_link(message, user_id)
                await _save_reward_data(db, user_id, link)
                await message.answer(reward_text, reply_markup=get_reward_link_button(link), protect_content=True)
        else:
            # First time accessing reward - generate new link
            link = await _generate_invite_link(message, user_id)
            await _save_reward_data(db, user_id, link)
            await message.answer(reward_text, reply_markup=get_reward_link_button(link), protect_content=True)
    else:
        # User doesn't have enough points yet
        remaining = db.required_referrals - valid_count
        reward_text = base_text + f"\n\n<i>📢 Yana {remaining} ta do'stingizni taklif qiling!</i>"

        await message.answer(reward_text)

async def _generate_invite_link(message: Message, user_id: int) -> str:
    """Generate invite link for Olympiad channel"""
    link_obj = await message.bot.create_chat_invite_link(
        chat_id=OLYMPIAD_CHANNEL_ID,
        name=f"Join link for {user_id}",
        member_limit=1
    )
    return link_obj.invite_link

async def _save_reward_data(db: Database, user_id: int, link: str):
    """Save reward data to database"""
    reward_data = {
        'links': [link]
    }
    await db.save_user_reward(user_id, reward_data)
