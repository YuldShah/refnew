from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from database.models import Database
from text.messages import get_text
from keyboards.user_keyboards import get_stats_keyboard
from services.referral_service import ReferralService

async def show_user_stats(message: Message, db: Database):
    """Display user's referral statistics"""
    referral_service = ReferralService(db)
    
    # Check and validate any pending referrals
    validation_result = await referral_service.check_and_validate_pending_referrals(
        message.from_user.id, message.bot
    )
    
    # Get updated stats after validation
    stats = await referral_service.get_referral_stats(message.from_user.id)
    
    # Create base text
    text = get_text('user_stats_message', 'uz', **stats)
    
    # Add validation result if any referrals were validated
    if validation_result["validated"] > 0:
        validation_text = get_text(
            'referrals_validated', 
            'uz', 
            count=validation_result["validated"]
        )
        text += f"\n\n{validation_text}"
    
    await message.answer(
        text,
        reply_markup=get_stats_keyboard()
    )

async def refresh_user_stats(callback: CallbackQuery, db: Database):
    """Handle refresh stats button press"""
    await callback.answer("🔄 Refreshing stats...")
    
    referral_service = ReferralService(db)
    
    # Check and validate any pending referrals
    validation_result = await referral_service.check_and_validate_pending_referrals(
        callback.from_user.id, callback.bot
    )
    
    # Get updated stats after validation
    stats = await referral_service.get_referral_stats(callback.from_user.id)
    
    # Create base text
    text = get_text('user_stats_message', 'uz', **stats)
    
    # Add validation result if any referrals were validated
    if validation_result["validated"] > 0:
        validation_text = get_text(
            'referrals_validated', 
            'uz', 
            count=validation_result["validated"]
        )
        text += f"\n\n{validation_text}"
    else:
        # Add refresh timestamp to make message different
        from datetime import datetime
        refresh_time = datetime.now().strftime("%H:%M")
        refresh_text = f"🔄 Oxirgi yangilanish: {refresh_time}"
        text += f"\n\n{refresh_text}"
    
    # Try to edit the message, but handle the case where content is the same
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_stats_keyboard()
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            # If message content is the same, just show a notification
            await callback.answer(get_text('stats_up_to_date', 'uz'), show_alert=True)
        else:
            # Re-raise other TelegramBadRequest exceptions
            raise e
