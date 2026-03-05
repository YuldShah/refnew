from aiogram import F, Router
from aiogram.types import InlineQuery, Message

from database.models import Database
from filters.user_filters import IsUserFilter
from text.messages import get_text


menu_router = Router()
menu_router.message.filter(IsUserFilter())


@menu_router.message(
    F.text.in_(
        [
            "📃 Qatnashish sharti 📃",
            "✅ Turbo marafon haqida ✅",
            "🔗 Taklif havolasi 🔗",
            "📈Ballarim📈",
            "🎁 Sovrinlar ⭐️",
            "📋 Qoidalar",
            "🚀 Kirish huquqini olish",
            "🔗 Mening taklif havolam",
            "📊 Mening statistikam",
        ]
    )
)
async def menu_button_handler(message: Message, db: Database):
    user = await db.get_user(message.from_user.id)
    if not user or not user.get("registration_completed"):
        await message.answer(get_text("register_first", "uz"))
        return

    if message.text in ["📃 Qatnashish sharti 📃", "📋 Qoidalar"]:
        from handlers.user.info_handlers import show_participation_requirements

        await show_participation_requirements(message, db)
    elif message.text in ["✅ Turbo marafon haqida ✅"]:
        from handlers.user.info_handlers import show_turbo_info

        await show_turbo_info(message, db)
    elif message.text in ["🔗 Taklif havolasi 🔗", "🔗 Mening taklif havolam"]:
        from handlers.user.referral_handlers import show_referral_link

        await show_referral_link(message, db)
    elif message.text in ["📈Ballarim📈", "📊 Mening statistikam", "🚀 Kirish huquqini olish"]:
        from handlers.user.stats_handlers import show_user_stats

        await show_user_stats(message, db)
    elif message.text in ["🎁 Sovrinlar ⭐️"]:
        from handlers.user.info_handlers import show_prizes

        await show_prizes(message, db)


@menu_router.inline_query()
async def handle_inline_query(inline_query: InlineQuery, db: Database):
    from handlers.user.referral_handlers import handle_inline_query

    await handle_inline_query(inline_query, db)
