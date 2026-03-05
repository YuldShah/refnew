import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from database.models import Database
from filters.user_filters import IsUserFilter
from handlers.user.access_helpers import (
    get_missing_channel_ids,
    send_entry_message,
    send_subscription_prompt,
)
from handlers.user.registration_states import RegistrationStates
from keyboards.user_keyboards import (
    get_contact_request_keyboard,
    get_education_status_keyboard,
    get_sat_goal_keyboard,
)
from text.messages import get_text


registration_router = Router()
registration_router.message.filter(IsUserFilter())
registration_router.callback_query.filter(IsUserFilter())

EDUCATION_OPTIONS = {
    "teacher": "o'qituvchi",
    "student": "talaba",
    "school_student": "o'quvchi",
}

SAT_GOAL_OPTIONS = {
    "grant": "grant uchun (1200+)",
    "ustama": "ustama uchun (700+)",
    "other": "boshqa",
}


async def _extract_referral_from_start(
    message: Message,
    db: Database,
    fallback_state_data: dict,
) -> tuple[dict | None, str | None, bool]:
    referrer = None
    referral_code = None

    args = message.text.split(maxsplit=1)
    if len(args) == 1:
        state_referrer_id = fallback_state_data.get("referrer_telegram_id")
        state_referral_code = fallback_state_data.get("referral_code")
        if state_referrer_id and state_referral_code:
            referrer = await db.get_user(state_referrer_id)
            referral_code = state_referral_code if referrer else None
        return referrer, referral_code, False

    param = args[1].strip()
    logging.info("Processing /start parameter: %s", param)

    if param == "sub":
        await send_subscription_prompt(message, db)
        return None, None, True

    if param == "access_denied":
        await message.answer(
            "🚫 <b>Kirish taqiqlangan</b>\n\nSizga bu botdan foydalanish taqiqlangan."
        )
        return None, None, True

    if len(param) == 8:
        referral_code = param
        referrer = await db.get_user_by_referral_code(referral_code)
        if not referrer or referrer["telegram_id"] == message.from_user.id:
            await message.answer(get_text("invalid_referral", "uz"))
            return None, None, False
        return referrer, referral_code, False

    await message.answer(get_text("invalid_referral", "uz"))
    return None, None, False


async def _notify_referrer_about_registration(
    target_message: Message,
    actor,
    db: Database,
    referrer_telegram_id: int | None,
    referral_code: str | None,
    collected_full_name: str,
):
    if not referrer_telegram_id or not referral_code:
        return

    referrer = await db.get_user(referrer_telegram_id)
    if not referrer:
        return

    referral_added = await db.add_referral(
        referrer["telegram_id"],
        actor.id,
        referral_code,
    )
    if not referral_added:
        return

    referrer_missing = await get_missing_channel_ids(target_message.bot, referrer["telegram_id"], db)
    user_missing = await get_missing_channel_ids(target_message.bot, actor.id, db)
    both_subscribed = not referrer_missing and not user_missing

    user_label = collected_full_name or (f"@{actor.username}" if actor.username else "User")
    user_mention = f'<a href="tg://user?id={actor.id}">{user_label}</a>'

    if both_subscribed:
        await db.validate_referral(referrer["telegram_id"], actor.id)
        notification_text = get_text(
            "referrer_new_user_subscribed",
            "uz",
            user_name=user_mention,
        )
    else:
        notification_text = get_text(
            "referrer_new_user_pending",
            "uz",
            user_name=user_mention,
        )

    try:
        await target_message.bot.send_message(referrer["telegram_id"], notification_text)
    except Exception as exc:
        logging.error(
            "Failed to send referrer notification to %s: %s",
            referrer["telegram_id"],
            exc,
        )


async def _finish_registration(
    target_message: Message,
    actor,
    state: FSMContext,
    db: Database,
    sat_goal_key: str,
):
    state_data = await state.get_data()
    sat_goal = SAT_GOAL_OPTIONS[sat_goal_key]
    collected_full_name = state_data["full_name"]

    await db.complete_user_registration(
        telegram_id=actor.id,
        username=actor.username or "",
        full_name=collected_full_name,
        age=state_data["age"],
        phone_number=state_data["phone_number"],
        education_status=state_data["education_status"],
        sat_goal=sat_goal,
    )

    await _notify_referrer_about_registration(
        target_message,
        actor,
        db,
        state_data.get("referrer_telegram_id"),
        state_data.get("referral_code"),
        collected_full_name,
    )

    await state.clear()
    await target_message.answer(
        "Rahmat. Ma'lumotlaringiz saqlandi.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await send_entry_message(
        target_message,
        db,
        actor.id,
        actor.mention_html(),
    )


async def _ask_sat_goal(target_message: Message, state: FSMContext, education_status: str):
    await state.update_data(education_status=education_status)
    await state.set_state(RegistrationStates.sat_goal)
    await target_message.answer("SAT sizga nimaga kerak?")
    await target_message.answer(
        "Quyidagi variantlardan birini tanlang.",
        reply_markup=get_sat_goal_keyboard(),
    )


@registration_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, db: Database):
    fallback_state_data = await state.get_data()
    await state.clear()

    referrer, referral_code, handled = await _extract_referral_from_start(
        message,
        db,
        fallback_state_data,
    )
    if handled:
        return

    existing_user = await db.get_user(message.from_user.id)
    if existing_user and existing_user.get("registration_completed"):
        await send_entry_message(
            message,
            db,
            message.from_user.id,
            message.from_user.mention_html(),
        )
        if referral_code:
            await message.answer(get_text("already_registered", "uz"))
        return

    await db.ensure_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "",
    )

    await state.update_data(
        referrer_telegram_id=referrer["telegram_id"] if referrer else None,
        referral_code=referral_code,
    )
    await state.set_state(RegistrationStates.full_name)
    await message.answer(
        "Assalomu alaykum. Ro'yxatdan o'tish uchun ism va familiyangizni yuboring."
    )


@registration_router.message(RegistrationStates.full_name)
async def process_full_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Iltimos, ism va familiyangizni matn ko'rinishida yuboring.")
        return

    full_name = " ".join(message.text.split())
    if len(full_name) < 3:
        await message.answer("Ism va familiya kamida 3 ta belgidan iborat bo'lishi kerak.")
        return

    await state.update_data(full_name=full_name)
    await state.set_state(RegistrationStates.age)
    await message.answer("Yoshingizni kiriting.")


@registration_router.message(RegistrationStates.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text or not message.text.strip().isdigit():
        await message.answer("Yoshni faqat raqam bilan yuboring.")
        return

    age = int(message.text.strip())
    if age < 7 or age > 100:
        await message.answer("Iltimos, to'g'ri yosh kiriting.")
        return

    await state.update_data(age=age)
    await state.set_state(RegistrationStates.phone_number)
    await message.answer(
        "Telefon raqamingizni yuboring.",
        reply_markup=get_contact_request_keyboard(),
    )


@registration_router.message(RegistrationStates.phone_number, F.contact)
async def process_phone_number(message: Message, state: FSMContext):
    if message.contact.user_id != message.from_user.id:
        await message.answer("Iltimos, o'zingizning telefon raqamingizni yuboring.")
        return

    await state.update_data(phone_number=message.contact.phone_number)
    await state.set_state(RegistrationStates.education_status)
    await message.answer(
        "Ta'limdagi maqomingizni tanlang.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(
        "Quyidagi inline tugmalardan birini bosing.",
        reply_markup=get_education_status_keyboard(),
    )


@registration_router.message(RegistrationStates.phone_number)
async def process_phone_number_invalid(message: Message):
    await message.answer(
        "Telefon raqamni pastdagi tugma orqali yuboring.",
        reply_markup=get_contact_request_keyboard(),
    )


@registration_router.message(RegistrationStates.education_status)
async def process_education_status_invalid(message: Message):
    await message.answer(
        "Iltimos, maqomni inline tugmalar orqali tanlang.",
        reply_markup=get_education_status_keyboard(),
    )


@registration_router.callback_query(
    RegistrationStates.education_status,
    F.data.startswith("education_status:"),
)
async def process_education_status(callback: CallbackQuery, state: FSMContext):
    education_status_key = callback.data.split(":", 1)[1]
    education_status = EDUCATION_OPTIONS.get(education_status_key)
    if not education_status:
        await callback.answer("Noto'g'ri variant.", show_alert=True)
        return

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await callback.answer("Maqom saqlandi.")
    await _ask_sat_goal(callback.message, state, education_status)


@registration_router.message(RegistrationStates.sat_goal)
async def process_sat_goal_invalid(message: Message):
    await message.answer("Iltimos, SAT maqsadini tugmalar orqali tanlang.")


@registration_router.callback_query(
    RegistrationStates.sat_goal,
    F.data.startswith("sat_goal:"),
)
async def process_sat_goal(callback: CallbackQuery, state: FSMContext, db: Database):
    sat_goal_key = callback.data.split(":", 1)[1]
    if sat_goal_key not in SAT_GOAL_OPTIONS:
        await callback.answer("Noto'g'ri variant.", show_alert=True)
        return

    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except Exception:
        pass

    await callback.answer("Ma'lumotlar saqlandi.")
    await _finish_registration(callback.message, callback.from_user, state, db, sat_goal_key)
