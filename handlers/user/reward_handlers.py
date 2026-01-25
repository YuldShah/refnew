from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.models import Database
from text.messages import get_text
from services.referral_service import ReferralService

# Reward channels/groups IDs
REWARD_CHANNELS = [
    {"id": -1003596736429, "name": "Muhokama guruh"},
    {"id": -1003828619807, "name": "0 dan 90 mlngacha kanali"},
    {"id": -1003839467045, "name": "0 dan 90 mlngacha guruhi"}
]

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
        # User has enough points - show reward with channel links
        reward_text = base_text + "\n\n<b>✅ Tabriklaymiz! Siz yopiq kanal va guruhimizga qo'shilishingiz mumkin!</b>\n\n👇 Quyidagi havolalar orqali qo'shiling:"

        # Check if user has already accessed reward
        if await db.has_user_accessed_reward(user_id):
            # Get existing reward data from database
            reward_data = await db.get_user_reward(user_id)
            if reward_data and 'links' in reward_data:
                # Use existing links
                links = reward_data['links'] if isinstance(reward_data['links'], list) else [reward_data['links']]
                keyboard = _create_reward_keyboard(links)
                await message.answer(reward_text, reply_markup=keyboard, protect_content=True)
            else:
                # Fallback: regenerate links if data is corrupted
                links = await _generate_invite_links(message, user_id)
                await _save_reward_data(db, user_id, links)
                keyboard = _create_reward_keyboard(links)
                await message.answer(reward_text, reply_markup=keyboard, protect_content=True)
        else:
            # First time accessing reward - generate new links
            links = await _generate_invite_links(message, user_id)
            await _save_reward_data(db, user_id, links)
            keyboard = _create_reward_keyboard(links)
            await message.answer(reward_text, reply_markup=keyboard, protect_content=True)
    else:
        # User doesn't have enough points yet
        remaining = db.required_referrals - valid_count
        reward_text = base_text + f"\n\n<i>📢 Yana {remaining} ta do'stingizni taklif qiling!</i>"

        await message.answer(reward_text)

async def _generate_invite_links(message: Message, user_id: int) -> list:
    """Generate invite links for all reward channels"""
    links = []
    for channel in REWARD_CHANNELS:
        try:
            link_obj = await message.bot.create_chat_invite_link(
                chat_id=channel["id"],
                name=f"User {user_id}",
                member_limit=1
            )
            links.append({"name": channel["name"], "url": link_obj.invite_link})
        except Exception as e:
            print(f"Error creating invite link for {channel['name']}: {e}")
            links.append({"name": channel["name"], "url": "#"})
    return links

def _create_reward_keyboard(links: list) -> InlineKeyboardMarkup:
    """Create inline keyboard with reward channel links"""
    buttons = []
    for i, link_data in enumerate(links):
        if isinstance(link_data, dict):
            buttons.append([InlineKeyboardButton(
                text=f"{'📢' if 'kanal' in link_data['name'].lower() else '💬'} {link_data['name']}",
                url=link_data['url']
            )])
        else:
            # Legacy format compatibility
            buttons.append([InlineKeyboardButton(text=f"Kanal {i+1}", url=link_data)])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def _save_reward_data(db: Database, user_id: int, links: list):
    """Save reward data to database"""
    reward_data = {
        'links': links
    }
    await db.save_user_reward(user_id, reward_data)
