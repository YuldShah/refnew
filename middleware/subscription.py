import logging
import os
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQuery,
    Message,
    TelegramObject,
)

from database.models import Database
from handlers.user.registration_states import REGISTRATION_STATE_NAMES
from text.messages import get_text


VALID_MEMBER_STATUSES = {"member", "administrator", "creator"}


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, db: Database):
        self.db = db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, InlineQuery):
            return await self._handle_inline_query(handler, event, data)

        if not isinstance(event, (Message, CallbackQuery)):
            return await handler(event, data)

        user = event.from_user
        bot = data["bot"]

        if self._is_admin(user.id):
            return await handler(event, data)

        if isinstance(event, Message) and event.text and event.text.startswith("/start"):
            return await handler(event, data)

        if isinstance(event, CallbackQuery) and event.data == "check_subscription":
            return await handler(event, data)

        state: FSMContext | None = data.get("state")
        if state:
            current_state = await state.get_state()
            if current_state in REGISTRATION_STATE_NAMES:
                return await handler(event, data)

        user_access = await self.db.check_user_access(user.id)
        if user_access is True:
            return await handler(event, data)
        if user_access is False:
            await self._send_access_denied(event)
            return

        missing_channel_ids, permission_error = await self._get_missing_channel_ids(bot, user.id)
        if permission_error:
            error_message = get_text("unexpected_error", "uz")
            if isinstance(event, Message):
                await event.answer(error_message)
            else:
                await event.answer(error_message, show_alert=True)
            return

        if missing_channel_ids:
            if state:
                await state.clear()

            keyboard = await self.create_subscription_keyboard(missing_channel_ids)
            if isinstance(event, Message):
                await event.answer(
                    get_text("subscription_required", "uz"),
                    reply_markup=keyboard,
                )
            else:
                await event.message.answer(
                    get_text("subscription_required", "uz"),
                    reply_markup=keyboard,
                )
                await event.answer()
            return

        return await handler(event, data)

    async def _handle_inline_query(self, handler, inline_query: InlineQuery, data: Dict[str, Any]) -> Any:
        if self._is_admin(inline_query.from_user.id):
            return await handler(inline_query, data)

        user_access = await self.db.check_user_access(inline_query.from_user.id)
        if user_access is True:
            return await handler(inline_query, data)
        if user_access is False:
            await inline_query.answer(
                [],
                switch_pm_text="Botga o'tish",
                switch_pm_parameter="access_denied",
            )
            return

        missing_channel_ids, _ = await self._get_missing_channel_ids(
            data["bot"],
            inline_query.from_user.id,
        )
        if missing_channel_ids:
            from handlers.user.referral_handlers import handle_inline_query_for_not_subbed

            await handle_inline_query_for_not_subbed(inline_query, self.db)
            return

        return await handler(inline_query, data)

    def _is_admin(self, user_id: int) -> bool:
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if not admin_ids_str:
            return False

        try:
            admin_ids = list(map(int, admin_ids_str.split(",")))
        except ValueError:
            return False

        return user_id in admin_ids

    async def _get_missing_channel_ids(self, bot, user_id: int) -> tuple[list[int], bool]:
        channel_ids = await self.db.get_mandatory_channel_ids()
        if not channel_ids:
            return [], False

        missing_channel_ids = []
        permission_error = False

        for channel_id in channel_ids:
            try:
                member = await bot.get_chat_member(channel_id, user_id)
                if member.status not in VALID_MEMBER_STATUSES:
                    missing_channel_ids.append(channel_id)
            except Exception as exc:
                logging.error(
                    "Error checking subscription for user %s in channel %s: %s",
                    user_id,
                    channel_id,
                    exc,
                )
                permission_error = True
                await self._notify_admin(bot, channel_id)

        return missing_channel_ids, permission_error

    async def _notify_admin(self, bot, channel_id: int):
        admin_ids_str = os.getenv("ADMIN_IDS", "")
        if not admin_ids_str:
            return

        try:
            admin_ids = list(map(int, admin_ids_str.split(",")))
        except ValueError:
            return

        for admin_id in admin_ids:
            try:
                await bot.send_message(
                    admin_id,
                    (
                        "Bot kanal obunasini tekshira olmayapti. "
                        f"Kanal ID: {channel_id}. Botni admin qiling."
                    ),
                )
            except Exception as exc:
                logging.error("Failed to notify admin %s: %s", admin_id, exc)

    async def _send_access_denied(self, event):
        text = "🚫 <b>Kirish taqiqlangan</b>\n\nSizga bu botdan foydalanish taqiqlangan."

        if isinstance(event, Message):
            await event.answer(text)
        else:
            await event.message.answer(text)
            await event.answer("Kirish taqiqlangan", show_alert=True)

    async def create_subscription_keyboard(
        self,
        channel_ids: list[int] | None = None,
    ) -> InlineKeyboardMarkup:
        channels = await self.db.get_mandatory_channels()
        if channel_ids is not None:
            channel_ids_set = set(channel_ids)
            channels = [channel for channel in channels if channel["chat_id"] in channel_ids_set]

        keyboard_rows = []
        for index in range(0, len(channels), 2):
            row = []
            for channel in channels[index:index + 2]:
                row.append(
                    InlineKeyboardButton(
                        text=channel["title"],
                        url=channel["link"],
                    )
                )
            keyboard_rows.append(row)

        keyboard_rows.append(
            [
                InlineKeyboardButton(
                    text=get_text("check_subscription", "uz"),
                    callback_data="check_subscription",
                )
            ]
        )

        return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
