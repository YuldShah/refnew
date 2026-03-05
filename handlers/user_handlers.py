import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.user.access_helpers import (
    get_missing_channel_ids,
    send_main_menu,
    send_subscription_prompt,
)
from handlers.user.menu_handlers import menu_router
from handlers.user.registration_handlers import registration_router
from handlers.user.stats_handlers import refresh_user_stats
from text.messages import get_text


user_router = Router()
user_router.include_router(registration_router)
user_router.include_router(menu_router)


@user_router.callback_query(F.data == "back_to_menu")
async def back_to_menu_handler(callback: CallbackQuery, db):
    await callback.message.delete()
    await send_main_menu(callback.message, callback.from_user.mention_html())
    await callback.answer()


@user_router.callback_query(F.data == "check_subscription")
async def check_subscription_handler(callback: CallbackQuery, db):
    missing_channel_ids = await get_missing_channel_ids(callback.bot, callback.from_user.id, db)

    if not missing_channel_ids:
        validation_result = await db.validate_user_referrals(callback.from_user.id)

        if validation_result["validated"] > 0:
            async with db.pool.acquire() as conn:
                referrers = await conn.fetch(
                    """
                    SELECT u.telegram_id
                    FROM referrals r
                    JOIN users u ON r.referrer_id = u.id
                    WHERE r.referred_id = (SELECT id FROM users WHERE telegram_id = $1)
                    AND r.valid = TRUE
                    """,
                    callback.from_user.id,
                )

            for referrer in referrers:
                user_label = callback.from_user.full_name or (
                    f"@{callback.from_user.username}" if callback.from_user.username else "User"
                )
                user_mention = f'<a href="tg://user?id={callback.from_user.id}">{user_label}</a>'
                notification_text = get_text(
                    "referrer_user_subscribed",
                    "uz",
                    user_name=user_mention,
                )
                try:
                    await callback.bot.send_message(referrer["telegram_id"], notification_text)
                except Exception as exc:
                    logging.error(
                        "Failed to send notification to referrer %s: %s",
                        referrer["telegram_id"],
                        exc,
                    )

        success_text = get_text("subscription_confirmed", "uz")
        try:
            await callback.message.edit_text(success_text)
        except Exception:
            await callback.message.answer(success_text)

        user = await db.get_user(callback.from_user.id)
        if user and user.get("registration_completed"):
            await send_main_menu(callback.message, callback.from_user.mention_html())
        else:
            await callback.message.answer(get_text("register_first", "uz"))
    else:
        await send_subscription_prompt(callback.message, db, missing_channel_ids)
        await callback.answer(get_text("not_subscribed", "uz"), show_alert=True)
        return

    await callback.answer()


@user_router.callback_query(F.data == "refresh_stats")
async def refresh_stats_handler(callback: CallbackQuery, db):
    await refresh_user_stats(callback, db)
