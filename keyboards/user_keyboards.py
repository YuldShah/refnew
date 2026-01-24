from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, SwitchInlineQueryChosenChat, CopyTextButton
from text.messages import get_text

def get_main_user_keyboard() -> ReplyKeyboardMarkup:
    """Get the main user reply keyboard for SAT marathon"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 SAT marafon haqida 📋")],
            [KeyboardButton(text="‼️ Marafonda qatnashish sharti ‼️")],
            [KeyboardButton(text="🎁 Sovrinlar ⭐️")],
            [KeyboardButton(text="🔗Taklif havolasi🔗")],
            [KeyboardButton(text="👇SAT imtixoni beradigan imkoniyatlar👇")],
            [KeyboardButton(text="📊Ballarim📊")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_stats_keyboard() -> InlineKeyboardMarkup:
    """Get stats inline keyboard for users (only refresh option)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_text('refresh_stats', 'uz'), callback_data='refresh_stats')
        ]
    ])
    return keyboard

def get_referral_share_keyboard(referral_link: str = "") -> InlineKeyboardMarkup:
    """Get referral link share inline keyboard (hardcoded Uzbek)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Taklif havolani nusxalash",
                copy_text=CopyTextButton(text=referral_link)
            )
        ],
        [InlineKeyboardButton(
            text=get_text('share_referral_link', 'uz'), 
            switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(allow_bot_chats=False, allow_channel_chats=True, allow_user_chats=True, allow_group_chats=True, query="Xabar yuklanishini kuting...")
        )]
    ])
    return keyboard

def get_reward_link_button(link: str) -> InlineKeyboardMarkup:
    """Get reward link inline keyboard for single Olympiad channel"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🏆 Olimpiada kanali",
                url=link
            )
        ]
    ])
    return keyboard
