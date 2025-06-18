from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from text.messages import get_text

def get_main_user_keyboard() -> ReplyKeyboardMarkup:
    """Get the main user reply keyboard with 4 options (hardcoded Uzbek)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text('rules_button', 'uz'))],
            [KeyboardButton(text=get_text('get_reward_button', 'uz'))],
            [KeyboardButton(text=get_text('my_referral_link_button', 'uz'))],
            [KeyboardButton(text=get_text('my_stats_button', 'uz'))]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_stats_keyboard() -> InlineKeyboardMarkup:
    """Get stats refresh inline keyboard (hardcoded Uzbek)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('refresh_stats', 'uz'), callback_data='refresh_stats')]
    ])
    return keyboard

def get_referral_share_keyboard(referral_link: str = "") -> InlineKeyboardMarkup:
    """Get referral link share inline keyboard (hardcoded Uzbek)"""
    share_text = f"🎉 Taklif havolam: {referral_link}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=get_text('share_referral_link', 'uz'), 
            switch_inline_query=share_text
        )]
    ])
    return keyboard
