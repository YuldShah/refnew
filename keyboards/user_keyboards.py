from aiogram.types import (
    CopyTextButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from text.messages import get_text
from text.user_content import (
    REGISTRATION_BACK_BUTTON_TEXT,
    REGISTRATION_SHARE_PHONE_BUTTON_TEXT,
)


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
                    text=REGISTRATION_SHARE_PHONE_BUTTON_TEXT,
                    request_contact=True,
                )
            ],
            [KeyboardButton(text=REGISTRATION_BACK_BUTTON_TEXT)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_back_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=REGISTRATION_BACK_BUTTON_TEXT)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_education_status_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👨‍🏫 O'qituvchi",
                    callback_data="education_status:teacher",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎓 Talaba",
                    callback_data="education_status:student",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧑‍🎓 O'quvchi",
                    callback_data="education_status:school_student",
                )
            ],
            [
                InlineKeyboardButton(
                    text=REGISTRATION_BACK_BUTTON_TEXT,
                    callback_data="registration_back:phone_number",
                )
            ],
        ]
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
            [
                InlineKeyboardButton(
                    text=REGISTRATION_BACK_BUTTON_TEXT,
                    callback_data="registration_back:education_status",
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
            ],
            [
                InlineKeyboardButton(
                    text="Taklif havolasini ulashish",
                    switch_inline_query=referral_link,
                )
            ]
        ]
    )


def get_reward_link_button(links: list) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Muhokama guruh", url=links[0])],
            [InlineKeyboardButton(text="SAT Elbek guruh", url=links[1])],
            [InlineKeyboardButton(text="SAT Elbek Iyun", url=links[2])],
        ]
    )
