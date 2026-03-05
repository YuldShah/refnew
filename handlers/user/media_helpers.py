from aiogram.types import Message

from text.user_content import media_is_configured


async def send_photo_or_text(
    message: Message,
    photo_id: str,
    caption: str,
    reply_markup=None,
):
    if media_is_configured(photo_id):
        return await message.answer_photo(
            photo=photo_id,
            caption=caption,
            reply_markup=reply_markup,
        )

    return await message.answer(
        caption,
        reply_markup=reply_markup,
    )
