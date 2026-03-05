from aiogram.types import CallbackQuery, Message

from database.models import Database
from handlers.user.reward_handlers import send_reward_access_if_eligible
from services.referral_service import ReferralService
from text.user_content import POINTS_TEXT


async def show_user_stats(message: Message, db: Database):
    referral_service = ReferralService(db)
    await referral_service.check_and_validate_pending_referrals(
        message.from_user.id,
        message.bot,
    )

    user_stats = await referral_service.get_referral_stats(message.from_user.id)
    valid_points = user_stats.get("valid_referrals", 0)
    user_name = message.from_user.mention_html()

    await message.answer(POINTS_TEXT.format(user_name=user_name, points=valid_points))
    await send_reward_access_if_eligible(message, db, valid_points)


async def refresh_user_stats(callback: CallbackQuery, db: Database):
    referral_service = ReferralService(db)
    await referral_service.check_and_validate_pending_referrals(
        callback.from_user.id,
        callback.bot,
    )

    user_stats = await referral_service.get_referral_stats(callback.from_user.id)
    valid_points = user_stats.get("valid_referrals", 0)
    user_name = callback.from_user.mention_html()

    try:
        await callback.message.edit_text(
            POINTS_TEXT.format(user_name=user_name, points=valid_points)
        )
    except Exception:
        await callback.message.answer(
            POINTS_TEXT.format(user_name=user_name, points=valid_points)
        )

    await send_reward_access_if_eligible(callback.message, db, valid_points)
    await callback.answer("Ballar yangilandi.")
