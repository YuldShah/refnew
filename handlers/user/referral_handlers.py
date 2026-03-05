from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    Message,
)

from database.models import Database
from handlers.user.media_helpers import send_photo_or_text
from keyboards.user_keyboards import get_referral_share_keyboard
from services.referral_service import ReferralService
from text.messages import get_text
from text.user_content import (
    REFERRAL_CAPTION,
    REFERRAL_FOLLOWUP_TEXT,
    REFERRAL_PHOTO_ID,
)


async def show_referral_link(message: Message, db: Database):
    referral_service = ReferralService(db)

    bot_info = await message.bot.get_me()
    referral_link = await referral_service.get_user_referral_link(
        message.from_user.id,
        bot_info.username,
    )

    if not referral_link:
        await message.answer(get_text("referral_link_error", "uz"))
        return

    promo_message = await send_photo_or_text(
        message,
        REFERRAL_PHOTO_ID,
        REFERRAL_CAPTION.format(referral_link=referral_link),
    )
    await promo_message.reply(
        REFERRAL_FOLLOWUP_TEXT,
        reply_markup=get_referral_share_keyboard(referral_link),
    )


async def handle_inline_query(inline_query: InlineQuery, db: Database):
    user = await db.get_user(inline_query.from_user.id)
    if not user:
        await inline_query.answer(
            [],
            cache_time=0,
            switch_pm_text="Avval botda ro'yxatdan o'ting!",
            switch_pm_parameter="register",
        )
        return

    bot_info = await inline_query.bot.get_me()
    referral_service = ReferralService(db)
    referral_link = await referral_service.get_user_referral_link(
        inline_query.from_user.id,
        bot_info.username,
    )
    if not referral_link:
        await inline_query.answer([], cache_time=0)
        return

    result = InlineQueryResultArticle(
        id=f"referral-{inline_query.from_user.id}",
        title="Taklif havolasi",
        description="Shaxsiy taklif havolangizni ulashing",
        input_message_content=InputTextMessageContent(
            message_text=(
                REFERRAL_CAPTION.format(referral_link=referral_link)
                + "\n\n"
                + REFERRAL_FOLLOWUP_TEXT
            ),
            parse_mode="HTML",
        ),
    )
    await inline_query.answer([result], cache_time=0)


async def handle_inline_query_for_not_subbed(inline_query: InlineQuery, db: Database):
    await inline_query.answer(
        [],
        cache_time=0,
        switch_pm_text="Avval bizning kanallarga obuna bo'ling!",
        switch_pm_parameter="sub",
    )
