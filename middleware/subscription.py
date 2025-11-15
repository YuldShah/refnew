import os
import logging
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, InlineQuery, InlineQueryResultVideo
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
        # Handle inline queries separately
        if isinstance(event, InlineQuery):
            return await self._handle_inline_query(handler, event, data)
            
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
            
            # Check manual access first
            user_access = await self.db.check_user_access(user.id)
            if user_access is True:
                # User has manual access granted
                return await handler(event, data)
            elif user_access is False:
                # User has manual access denied
                await self._send_access_denied(event)
                return
            
            # Check mandatory channels (normal flow)
            channel_ids = await self.db.get_mandatory_channel_ids()
            if not channel_ids:
                return await handler(event, data)
                
            unsubscribed_channels = []
            bot_permission_error = False
            for channel_id in channel_ids:
                try:
                    member = await bot.get_chat_member(channel_id, user.id)
                    # Check if user is NOT a full member (consistent with referral validation)
                    if member.status not in ['member', 'administrator', 'creator']:
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
                
                keyboard = await self.create_subscription_keyboard()
                
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

    async def _handle_inline_query(self, handler, inline_query: InlineQuery, data: Dict[str, Any]) -> Any:
        """Handle inline queries with subscription checking"""
        user = inline_query.from_user
        bot = data['bot']
        print("Inline query")
        # Skip subscription check for admins
        admin_ids_str = os.getenv('ADMIN_IDS', '')
        if admin_ids_str:
            admin_ids = list(map(int, admin_ids_str.split(',')))
            if user.id in admin_ids:
                return await handler(inline_query, data)
        
        # Check manual access first
        user_access = await self.db.check_user_access(user.id)
        if user_access is True:
            # User has manual access granted
            return await handler(inline_query, data)
        elif user_access is False:
            # User has manual access denied - show switch_pm
            await inline_query.answer(
                [],
                switch_pm_text="Botga o'tish",
                switch_pm_parameter="access_denied"
            )
            return
        
        # Check mandatory channels
        channel_ids = await self.db.get_mandatory_channel_ids()
        if not channel_ids:
            return await handler(inline_query, data)
            
        unsubscribed_channels = []
        for channel_id in channel_ids:
            try:
                member = await bot.get_chat_member(channel_id, user.id)
                if member.status in ['left', 'kicked']:
                    unsubscribed_channels.append(channel_id)
            except Exception as e:
                logging.error(f"Error checking subscription for channel {channel_id}: {e}")
        
        print(unsubscribed_channels)
        if unsubscribed_channels:
            # User not subscribed - use the dedicated handler
            from handlers.user.referral_handlers import handle_inline_query_for_not_subbed
            await handle_inline_query_for_not_subbed(inline_query, self.db)
            return
        
        # User is subscribed - proceed with handler
        return await handler(inline_query, data)

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
    
    async def _send_access_denied(self, event):
        """Send access denied message"""
        from text.messages import get_text
        text = "🚫 <b>Kirish taqiqlangan</b>\n\n"
        text += "Sizga bu botdan foydalanish taqiqlangan."
        
        if isinstance(event, Message):
            await event.answer(text)
        elif isinstance(event, CallbackQuery):
            await event.message.answer(text)
            await event.answer("Kirish taqiqlangan", show_alert=True)
    
    async def create_subscription_keyboard(self) -> InlineKeyboardMarkup:
        """Create subscription keyboard with actual mandatory channels"""
        from text.messages import get_text
        
        channels = await self.db.get_mandatory_channels()
        keyboard_rows = []
        
        # Add channel buttons (max 2 per row)
        for i in range(0, len(channels), 2):
            row = []
            for j in range(i, min(i + 2, len(channels))):
                channel = channels[j]
                row.append(InlineKeyboardButton(
                    text=channel['title'],
                    url=channel['link']
                ))
            keyboard_rows.append(row)
        
        # Add check subscription button
        keyboard_rows.append([
            InlineKeyboardButton(
                text=get_text('check_subscription', 'uz'),
                callback_data='check_subscription'
            )
        ])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
