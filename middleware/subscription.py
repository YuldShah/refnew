import os
import logging
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from typing import Callable, Dict, Any, Awaitable
from database.models import Database
from text.messages import get_text

class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self, db: Database):
        self.db = db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            user = event.from_user
            bot = data['bot']
            
            # Skip subscription check for admins
            admin_ids_str = os.getenv('ADMIN_IDS', '')
            if admin_ids_str:
                admin_ids = list(map(int, admin_ids_str.split(',')))
                if user.id in admin_ids:
                    return await handler(event, data)
              # Skip for certain commands and check_subscription callback
            if isinstance(event, Message) and event.text:
                if event.text.startswith('/start'):
                    return await handler(event, data)
            
            # Skip subscription check for check_subscription callback to let handler handle it
            if isinstance(event, CallbackQuery) and event.data == 'check_subscription':
                return await handler(event, data)
            
            from text.messages import get_text
            
            channel_ids = self.db.get_mandatory_channel_ids()
            if not channel_ids:
                return await handler(event, data)
                
            unsubscribed_channels = []
            bot_permission_error = False
            
            for channel_id in channel_ids:
                try:
                    member = await bot.get_chat_member(channel_id, user.id)
                    if member.status in ['left', 'kicked']:
                        unsubscribed_channels.append(channel_id)
                except TelegramForbiddenError:
                    bot_permission_error = True
                    logging.error(f"Bot has no permission to check membership in channel {channel_id}")
                    await self._notify_admin(bot, channel_id)
                except Exception as e:
                    logging.error(f"Error checking subscription for channel {channel_id}: {e}")
                    bot_permission_error = True
            
            if bot_permission_error:
                error_message = get_text('unexpected_error', 'uz')
                
                if isinstance(event, Message):
                    await event.answer(error_message)
                elif isinstance(event, CallbackQuery):
                    await event.answer(error_message, show_alert=True)
                return
            
            if unsubscribed_channels:
                # Clear state if exists
                state: FSMContext = data.get('state')
                if state:
                    await state.clear()
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text=get_text('our_chats_folder', 'uz'),
                        url="https://t.me/addlist/a55Whe4Fa9ozNDky"
                    )],
                    [InlineKeyboardButton(
                        text=get_text('check_subscription', 'uz'),
                        callback_data='check_subscription'
                    )]                ])
                
                try:
                    if isinstance(event, Message):
                        await event.answer(
                            get_text('subscription_required', 'uz'),
                            reply_markup=keyboard
                        )
                    elif isinstance(event, CallbackQuery):
                        await event.message.edit_text(
                            get_text('subscription_required', 'uz'),
                            reply_markup=keyboard
                        )
                except TelegramBadRequest as e:
                    if "message is not modified" in str(e):
                        if isinstance(event, CallbackQuery):
                            await event.answer()
                    else:
                        logging.error(f"Error editing message: {e}")
                
                return
        
        return await handler(event, data)

    async def _notify_admin(self, bot, channel_id):
        """Notify admin about bot permission issues"""
        try:
            admin_ids_str = os.getenv('ADMIN_IDS', '')
            if admin_ids_str:
                admin_ids = list(map(int, admin_ids_str.split(',')))
                for admin_id in admin_ids:
                    try:
                        await bot.send_message(
                            admin_id, 
                            f"⚠️ Bot doesn't have permission to check membership in channel {channel_id}. Please add bot as admin."
                        )
                    except Exception as e:
                        logging.error(f"Failed to notify admin {admin_id}: {e}")
        except Exception as e:
            logging.error(f"Error in _notify_admin: {e}")
