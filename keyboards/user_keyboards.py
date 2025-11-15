from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, SwitchInlineQueryChosenChat, CopyTextButton
from text.messages import get_text

def get_main_user_keyboard() -> ReplyKeyboardMarkup:
    """Get the main user reply keyboard with 4 rows (hardcoded Uzbek)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📋 SAT marafon haqida 📋')],
            [KeyboardButton(text='‼️ Marafonda qatnashish sharti ‼️'), KeyboardButton(text='🎁 Sovrinlar ⭐️')],
            [KeyboardButton(text='🔗Taklif havolasi🔗'), KeyboardButton(text='📊Ballarim📊')],
            [KeyboardButton(text='👇SAT imtixoni beradigan imkoniyatlar👇')]
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
                text="Referral havolani nusxalash",
                copy_text=CopyTextButton(text=referral_link)
            )
        ],
        [InlineKeyboardButton(
            text=get_text('share_referral_link', 'uz'), 
            switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(allow_bot_chats=False, allow_channel_chats=True, allow_user_chats=True, allow_group_chats=True, query="Xabar yuklanishini kuting...")
        )]
    ])
    return keyboard

def get_reward_link_button(invite_data: list) -> InlineKeyboardMarkup:
    """Get reward link inline keyboard - dynamically generated from config"""
    buttons = []
    for item in invite_data:
        buttons.append([
            InlineKeyboardButton(
                text=item['name'],
                url=item['link']
            )
        ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_press_referral_link_button(referral_link) -> InlineKeyboardMarkup:
    """Get button prompting user to press referral link button (hardcoded Uzbek)"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🏆 Marafonda qatnashish 🏆",
                url=referral_link
            )
        ]
    ])
    return keyboard