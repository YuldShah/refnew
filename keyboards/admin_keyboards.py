from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from text.messages import get_text

def admin_main_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Admin main menu reply keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text('admin_top_referrers', language))],
            [KeyboardButton(text=get_text('admin_user_lookup', language))],
            [KeyboardButton(text=get_text('admin_export_data', language))],
            [KeyboardButton(text=get_text('admin_stats', language))]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard
