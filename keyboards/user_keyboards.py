from aiogram.types import (
    CopyTextButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from text.messages import get_text


def get_main_user_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📃 Qatnashish sharti 📃"),
                KeyboardButton(text="✅ Turbo marafon haqida ✅"),
            ],
            [
                KeyboardButton(text="🔗 Taklif havolasi 🔗"),
                KeyboardButton(text="📈Ballarim📈"),
            ],
            [KeyboardButton(text="🎁 Sovrinlar ⭐️")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


def get_contact_request_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Telefon raqamni yuborish",
                    request_contact=True,
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_education_status_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="O'qituvchi")],
            [KeyboardButton(text="Talaba")],
            [KeyboardButton(text="O'quvchi")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_sat_goal_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Grant uchun (1200+)",
                    callback_data="sat_goal:grant",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Ustama uchun (700+)",
                    callback_data="sat_goal:ustama",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Boshqa",
                    callback_data="sat_goal:other",
                )
            ],
        ]
    )


def get_stats_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_text("refresh_stats", "uz"),
                    callback_data="refresh_stats",
                )
            ]
        ]
    )


def get_referral_share_keyboard(referral_link: str = "") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Taklif havolasini nusxalash",
                    copy_text=CopyTextButton(text=referral_link),
                )
            ]
        ]
    )


def get_reward_link_button(links: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Yopiq kanal", url=links[1])],
            [InlineKeyboardButton(text="Yopiq guruh", url=links[0])],
            [InlineKeyboardButton(text="Muhokama guruhi", url=links[2])],
        ]
    )
