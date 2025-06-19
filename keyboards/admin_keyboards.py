from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from text.messages import get_text

def admin_main_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Admin main menu reply keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text('admin_stats', language))],
            [KeyboardButton(text=get_text('admin_manage_access', language))]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_admin_stats_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """Admin stats inline keyboard with sub-options"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text('refresh_stats', language),
                    callback_data='admin_refresh_stats'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text('admin_top_referrers', language),
                    callback_data='admin_top_10'
                ),
                InlineKeyboardButton(
                    text=get_text('admin_user_lookup', language),
                    callback_data='admin_find_user'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text('admin_export_data', language),
                    callback_data='admin_export'
                )
            ]
        ]
    )
    return keyboard

def get_manage_access_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """Main manage access keyboard"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text('mandatory_channels_btn', language),
                    callback_data='mandatory_channels'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text('manual_access_btn', language),
                    callback_data='manual_access'
                )
            ]
        ]
    )
    return keyboard

def get_mandatory_channels_keyboard(language: str = 'uz', channels: list = None) -> InlineKeyboardMarkup:
    """Mandatory channels management keyboard"""
    buttons = []
    
    # Delete buttons for existing channels
    if channels:
        for channel in channels:
            buttons.append([
                InlineKeyboardButton(
                    text=f"{channel['title']}", 
                    url=channel['link']
                ),
                InlineKeyboardButton(
                    text=f"🗑 O'chirish",
                    callback_data=f'delete_channel_{channel["chat_id"]}'
                )
            ])
        
    
    # Add channel button
    buttons.append([
        InlineKeyboardButton(
            text=get_text('add_channel_btn', language),
            callback_data='add_mandatory_channel'
        )
    ])

    if channels:
        # Reset all button
        buttons.append([
            InlineKeyboardButton(
                text=get_text('reset_all_channels_btn', language),
                callback_data='reset_all_channels'
            )
        ])
    
    # Back button
    buttons.append([
        InlineKeyboardButton(
            text=get_text('back_btn', language),
            callback_data='back_to_access'
        )
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def get_manual_access_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """Manual access management keyboard"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text('add_user_access_btn', language),
                    callback_data='add_user_access'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text('remove_user_access_btn', language),
                    callback_data='remove_user_access'
                )
            ],
            [
                InlineKeyboardButton(
                    text=get_text('back_btn', language),
                    callback_data='back_to_access'
                )
            ]
        ]
    )
    return keyboard

def get_confirm_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """Confirmation keyboard"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text('confirm_btn', language),
                    callback_data='confirm'
                ),
                InlineKeyboardButton(
                    text=get_text('cancel_btn', language),
                    callback_data='cancel'
                )
            ]
        ]
    )
    return keyboard

def get_top_referrers_keyboard(language: str = 'uz') -> InlineKeyboardMarkup:
    """Keyboard for top referrers with refresh and close buttons"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text('refresh_stats', language),
                    callback_data='admin_refresh_top_10'
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Yopish",
                    callback_data='admin_close_message'
                )
            ]
        ]
    )
    return keyboard

def get_cancel_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Cancel keyboard for user search"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_main_menu_keyboard(language: str = 'uz') -> ReplyKeyboardMarkup:
    """Main menu keyboard for admins"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_text('back_to_admin_menu', language))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
