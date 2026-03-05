import logging

from database.models import Database
from keyboards.user_keyboards import get_main_user_keyboard
from middleware.subscription import SubscriptionMiddleware
from text.messages import get_text
from text.user_content import MAIN_MENU_TEXT


VALID_MEMBER_STATUSES = {"member", "administrator", "creator"}


async def get_missing_channel_ids(bot, user_id: int, db: Database) -> list[int]:
    channel_ids = await db.get_mandatory_channel_ids()
    missing_channel_ids = []

    for channel_id in channel_ids:
        try:
            member = await bot.get_chat_member(channel_id, user_id)
            if member.status not in VALID_MEMBER_STATUSES:
                missing_channel_ids.append(channel_id)
        except Exception as exc:
            logging.error(
                "Failed to check subscription for user %s in channel %s: %s",
                user_id,
                channel_id,
                exc,
            )
            missing_channel_ids.append(channel_id)

    return missing_channel_ids


async def send_subscription_prompt(message, db: Database, missing_channel_ids: list[int] | None = None):
    middleware = SubscriptionMiddleware(db)
    keyboard = await middleware.create_subscription_keyboard(missing_channel_ids)
    await message.answer(
        get_text("subscription_required", "uz"),
        reply_markup=keyboard,
    )


async def send_main_menu(message, mention_html: str):
    await message.answer(
        MAIN_MENU_TEXT.format(user_name=mention_html),
        reply_markup=get_main_user_keyboard(),
    )


async def send_entry_message(message, db: Database, user_id: int, mention_html: str) -> bool:
    missing_channel_ids = await get_missing_channel_ids(message.bot, user_id, db)
    if missing_channel_ids:
        await send_subscription_prompt(message, db, missing_channel_ids)
        return False

    await send_main_menu(message, mention_html)
    return True
