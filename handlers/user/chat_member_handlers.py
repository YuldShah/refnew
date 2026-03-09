import html
import logging

from aiogram import Router
from aiogram.types import ChatMemberUpdated, User

from database.models import Database
from handlers.user.access_helpers import VALID_MEMBER_STATUSES, get_missing_channel_ids
from handlers.user.reward_handlers import PRIVATE_REWARD_CHAT_IDS
from services.referral_service import ReferralService
from text.messages import get_text


chat_member_router = Router()

REWARD_CHAT_MEMBER_STATUSES = VALID_MEMBER_STATUSES | {"restricted"}


def _build_user_mention(user: User) -> str:
    display_name = user.full_name or (f"@{user.username}" if user.username else "User")
    return user.mention_html(display_name)


async def _safe_send_message(bot, user_id: int, text: str):
    try:
        await bot.send_message(user_id, text)
    except Exception as exc:
        logging.error("Failed to send chat-member notification to %s: %s", user_id, exc)


async def _revoke_reward_chat_access(bot, user_id: int):
    for chat_id in PRIVATE_REWARD_CHAT_IDS:
        try:
            member = await bot.get_chat_member(chat_id, user_id)
        except Exception as exc:
            logging.error(
                "Failed to inspect reward chat membership for user %s in chat %s: %s",
                user_id,
                chat_id,
                exc,
            )
            continue

        if member.status not in REWARD_CHAT_MEMBER_STATUSES:
            continue

        try:
            await bot.ban_chat_member(chat_id, user_id)
            await bot.unban_chat_member(chat_id, user_id, only_if_banned=True)
        except Exception as exc:
            logging.error(
                "Failed to revoke reward chat access for user %s in chat %s: %s",
                user_id,
                chat_id,
                exc,
            )


async def _handle_member_left(event: ChatMemberUpdated, db: Database, referred_telegram_id: int):
    referrer_telegram_id = await db.get_referrer_of_user(referred_telegram_id)
    if not referrer_telegram_id:
        return

    referral_invalidated = await db.invalidate_referral(referrer_telegram_id, referred_telegram_id)
    if not referral_invalidated:
        return

    valid_count = await db.get_valid_referrals_count(referrer_telegram_id)
    lang = await db.get_user_language(referrer_telegram_id)
    channel_name = html.escape(event.chat.title or "majburiy chat")
    referred_user = event.new_chat_member.user

    await _safe_send_message(
        event.bot,
        referrer_telegram_id,
        get_text(
            "referral_invalidated",
            lang,
            user_name=_build_user_mention(referred_user),
            channel_name=channel_name,
            current_referrals=valid_count,
            required_referrals=db.required_referrals,
        ),
    )

    if valid_count >= db.required_referrals:
        return

    if not await db.has_user_accessed_reward(referrer_telegram_id):
        return

    await _revoke_reward_chat_access(event.bot, referrer_telegram_id)
    await db.delete_user_reward(referrer_telegram_id)
    await _safe_send_message(
        event.bot,
        referrer_telegram_id,
        get_text(
            "reward_access_revoked",
            lang,
            current_referrals=valid_count,
            required_referrals=db.required_referrals,
        ),
    )


async def _handle_member_rejoined(event: ChatMemberUpdated, db: Database, referred_telegram_id: int):
    referrer_telegram_id = await db.get_referrer_of_user(referred_telegram_id)
    if not referrer_telegram_id:
        return

    missing_channel_ids = await get_missing_channel_ids(event.bot, referred_telegram_id, db)
    if missing_channel_ids:
        return

    referral_validated = await db.validate_referral(referrer_telegram_id, referred_telegram_id)
    if not referral_validated:
        return

    referral_service = ReferralService(db)
    await referral_service.check_and_notify_reward_eligibility(referrer_telegram_id, event.bot)


@chat_member_router.chat_member()
async def handle_mandatory_chat_member_update(event: ChatMemberUpdated, db: Database):
    target_user = event.new_chat_member.user
    if target_user.is_bot:
        return

    mandatory_channel_ids = await db.get_mandatory_channel_ids()
    if event.chat.id not in mandatory_channel_ids:
        return

    was_active = event.old_chat_member.status in VALID_MEMBER_STATUSES
    is_active = event.new_chat_member.status in VALID_MEMBER_STATUSES

    if was_active and not is_active:
        await _handle_member_left(event, db, target_user.id)
    elif not was_active and is_active:
        await _handle_member_rejoined(event, db, target_user.id)