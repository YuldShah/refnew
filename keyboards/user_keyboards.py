from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, SwitchInlineQueryChosenChat
from text.messages import get_text

def get_main_user_keyboard() -> ReplyKeyboardMarkup:
    """Get the main user reply keyboard with 4 options (hardcoded Uzbek)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text('get_reward_button', 'uz'))],
            [KeyboardButton(text=get_text('my_referral_link_button', 'uz'))],
            [KeyboardButton(text=get_text('my_stats_button', 'uz'))]
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
        [InlineKeyboardButton(
            text=get_text('share_referral_link', 'uz'), 
            switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(allow_bot_chats=False, allow_channel_chats=True, allow_user_chats=True, allow_group_chats=True)
        )]
    ])
    return keyboard

def get_reward_link_button(reward_link: str = "") -> InlineKeyboardMarkup:
    """Get reward link inline keyboard (hardcoded Uzbek)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📂 SAT Elbek",
                url=reward_link
            )
        ]
    ])
    return keyboard
