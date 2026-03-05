from aiogram.types import Message

from database.models import Database
from handlers.user.media_helpers import send_photo_or_text
from text.user_content import (
    PARTICIPATION_CAPTION,
    PARTICIPATION_PHOTO_ID,
    PRIZES_CAPTION,
    PRIZES_PHOTO_ID,
    TURBO_INFO_CAPTION,
    TURBO_INFO_PHOTO_ID,
)


async def show_participation_requirements(message: Message, db: Database):
    await send_photo_or_text(
        message,
        PARTICIPATION_PHOTO_ID,
        PARTICIPATION_CAPTION,
    )


async def show_turbo_info(message: Message, db: Database):
    await send_photo_or_text(
        message,
        TURBO_INFO_PHOTO_ID,
        TURBO_INFO_CAPTION,
    )


async def show_prizes(message: Message, db: Database):
    await send_photo_or_text(
        message,
        PRIZES_PHOTO_ID,
        PRIZES_CAPTION,
    )
