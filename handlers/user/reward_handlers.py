from aiogram.types import Message

from database.models import Database
from handlers.user.media_helpers import send_photo_or_text
from keyboards.user_keyboards import get_reward_link_button
from services.referral_service import ReferralService
from text.user_content import ACCESS_READY_TEXT, PRIZES_CAPTION, PRIZES_PHOTO_ID


PRIVATE_REWARD_CHAT_IDS = (
    -1003640124334,
    -1003545085346,
    -1003712836334,
)


async def show_rewards(message: Message, db: Database):
    await send_photo_or_text(
        message,
        PRIZES_PHOTO_ID,
        PRIZES_CAPTION,
    )


async def send_reward_access_if_eligible(
    message: Message,
    db: Database,
    valid_count: int | None = None,
):
    referral_service = ReferralService(db)
    if valid_count is None:
        stats = await referral_service.get_referral_stats(message.from_user.id)
        valid_count = stats.get("valid_referrals", 0)

    if valid_count < db.required_referrals:
        return False

    if await db.has_user_accessed_reward(message.from_user.id):
        reward_data = await db.get_user_reward(message.from_user.id)
        links = reward_data.get("links") if reward_data else None
        if not links:
            links = await _generate_invite_links(message, message.from_user.id)
            await _save_reward_data(db, message.from_user.id, links)
    else:
        links = await _generate_invite_links(message, message.from_user.id)
        await _save_reward_data(db, message.from_user.id, links)

    await message.answer(
        ACCESS_READY_TEXT,
        reply_markup=get_reward_link_button(links),
        protect_content=True,
    )
    return True


async def _generate_invite_links(message: Message, user_id: int) -> list:
    link1_obj = await message.bot.create_chat_invite_link(
        chat_id=PRIVATE_REWARD_CHAT_IDS[0],
        name=f"Join link for {user_id}",
        member_limit=1,
    )
    link2_obj = await message.bot.create_chat_invite_link(
        chat_id=PRIVATE_REWARD_CHAT_IDS[1],
        name=f"Join link for {user_id}",
        member_limit=1,
    )
    link3_obj = await message.bot.create_chat_invite_link(
        chat_id=PRIVATE_REWARD_CHAT_IDS[2],
        name=f"Join link for {user_id}",
        member_limit=1,
    )
    return [link1_obj.invite_link, link2_obj.invite_link, link3_obj.invite_link]


async def _save_reward_data(db: Database, user_id: int, links: list):
    reward_data = {"links": links}
    await db.save_user_reward(user_id, reward_data)
