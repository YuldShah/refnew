from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.models import Database
from text.messages import get_text
from services.referral_service import ReferralService
from services.admin_service import AdminService
from keyboards.admin_keyboards import get_admin_stats_keyboard, get_top_referrers_keyboard, get_cancel_keyboard, admin_main_keyboard
import logging
import os

# States for admin operations
class AdminStatsStates(StatesGroup):
    waiting_for_search_user_id = State()

async def show_admin_stats(message: Message, db: Database):
    """Display overall bot statistics for admins"""
    # Send menu change notification
    await message.answer(
        "📊 <b>Statistika menusi</b>",
        reply_markup=admin_main_keyboard()
    )
    
    # Get overall bot stats (excluding admin user with telegram_id = 19)
    async with db.pool.acquire() as conn:
        total_users = await conn.fetchval('SELECT COUNT(*) FROM users WHERE telegram_id != 19')
        total_valid_referrals = await conn.fetchval('''
            SELECT COUNT(*) FROM referrals r 
            JOIN users u1 ON r.referrer_id = u1.id 
            JOIN users u2 ON r.referred_id = u2.id 
            WHERE r.valid = TRUE AND u1.telegram_id != 19 AND u2.telegram_id != 19
        ''')
        total_pending_referrals = await conn.fetchval('''
            SELECT COUNT(*) FROM referrals r 
            JOIN users u1 ON r.referrer_id = u1.id 
            JOIN users u2 ON r.referred_id = u2.id 
            WHERE r.valid = FALSE AND u1.telegram_id != 19 AND u2.telegram_id != 19
        ''')
    
    reward_access_count = await db.get_reward_access_count()
    
    # Create overall bot stats text
    text = f"📈 <b>Umumiy bot statistikasi:</b>\n\n"
    text += f"<blockquote>👥 Foydalanuvchilar: <b>{total_users}</b>\n"
    text += f"✅ Tasdiqlangan takliflar: <b>{total_valid_referrals}</b>\n"
    text += f"⏳ Kutilayotgan takliflar: <b>{total_pending_referrals}</b>\n"
    text += f"🔓 Kirish huquqini olganlar: <b>{reward_access_count}</b></blockquote>"
    
    await message.answer(
        text,
        reply_markup=get_admin_stats_keyboard()
    )

async def show_top_10_users(callback: CallbackQuery, db: Database):
    """Show top 10 referrers to admin"""
    await callback.answer()
    
    admin_service = AdminService(db)
    top_referrers = await admin_service.get_top_referrers(10)
    
    text = "🏆 <b>TOP 10 Referrerlar:</b>\n\n"
    
    if not top_referrers:
        text += "Hali referal yo'q"
    else:
        text += "<blockquote>"
        for i, user in enumerate(top_referrers, 1):
            username = user['username'] or "Noma'lum"
            first_name = user['full_name'].split()[0] if user['full_name'] else "Foydalanuvchi"
            text += f"{i}. {first_name} (@{username}) - {user['referral_count']} ta taklif\n"
        text += "</blockquote>"

    await callback.message.answer(
        text,
        reply_markup=get_top_referrers_keyboard()
    )

async def search_user_request(callback: CallbackQuery, state: FSMContext):
    """Request user ID for search (admin only)"""
    await callback.answer()
    await state.set_state(AdminStatsStates.waiting_for_search_user_id)
    
    text = "🔍 <b>Foydalanuvchini qidirish</b>\n\n"
    text += "Qidirish uchun foydalanuvchi ID raqamini kiriting:\n"
    text += "Masalan: <code>123456789</code>"
    
    await callback.message.answer(
        text,
        reply_markup=get_cancel_keyboard()
    )

async def process_user_search(message: Message, state: FSMContext, db: Database):
    """Process user search by ID (admin only)"""
    # Check for cancel
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer(
            "🔍 Qidiruv bekor qilindi",
            reply_markup=admin_main_keyboard()
        )
        return
    
    await state.clear()
    
    try:
        user_id = int(message.text.strip())
        admin_service = AdminService(db)
        user_info = await admin_service.get_user_by_telegram_id(user_id)
        
        if not user_info:
            await message.answer(
                "⚠️ Foydalanuvchi topilmadi",
                reply_markup=admin_main_keyboard()
            )
            return
        
        # Format full user info for admin
        username = user_info.get('username') or "Noma'lum"
        full_name = user_info['full_name'] or "Noma'lum"
        
        text = f"👤 <b>Foydalanuvchi ma'lumotlari:</b>\n\n"
        text += f"🆔 ID: <code>{user_info['telegram_id']}</code>\n"
        text += f"👤 To'liq ism: {full_name}\n"
        text += f"📱 Username: @{username}\n"
        text += f"🔗 Referal kod: <code>{user_info['referral_code']}</code>\n"
        text += f"📅 Qo'shilgan: {user_info['joined_at'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        text += f"📊 <b>Statistika:</b>\n"
        text += f"✅ Tasdiqlangan takliflar: {user_info['valid_referrals'] or 0}\n"
        text += f"⏳ Kutilayotgan takliflar: {user_info['pending_referrals'] or 0}\n"
        text += f"📊 Jami takliflar: {(user_info['valid_referrals'] or 0) + (user_info['pending_referrals'] or 0)}"
        
        await message.answer(
            text,
            reply_markup=admin_main_keyboard()
        )
        
    except ValueError:
        await message.answer(
            "⚠️ Noto'g'ri format! Raqam kiriting.",
            reply_markup=admin_main_keyboard()
        )


async def refresh_admin_stats(callback: CallbackQuery, db: Database):
    """Refresh admin statistics"""
    await callback.answer("🔄 Refreshing admin stats...")
    
    # Get overall bot stats (excluding admin user with telegram_id = 19)
    async with db.pool.acquire() as conn:
        total_users = await conn.fetchval('SELECT COUNT(*) FROM users WHERE telegram_id != 19')
        total_valid_referrals = await conn.fetchval('''
            SELECT COUNT(*) FROM referrals r 
            JOIN users u1 ON r.referrer_id = u1.id 
            JOIN users u2 ON r.referred_id = u2.id 
            WHERE r.valid = TRUE AND u1.telegram_id != 19 AND u2.telegram_id != 19
        ''')
        total_pending_referrals = await conn.fetchval('''
            SELECT COUNT(*) FROM referrals r 
            JOIN users u1 ON r.referrer_id = u1.id 
            JOIN users u2 ON r.referred_id = u2.id 
            WHERE r.valid = FALSE AND u1.telegram_id != 19 AND u2.telegram_id != 19
        ''')
    
    reward_access_count = await db.get_reward_access_count()
    
    # Create overall bot stats text
    text = f"📈 <b>Umumiy bot statistikasi:</b>\n"
    text += f"<blockquote>👥 Foydalanuvchilar: <b>{total_users}</b>\n"
    text += f"✅ Tasdiqlangan takliflar: <b>{total_valid_referrals}</b>\n"
    text += f"⏳ Kutilayotgan takliflar: <b>{total_pending_referrals}</b>\n"
    text += f"🔓 Kirish huquqini olganlar: <b>{reward_access_count}</b></blockquote>"
    
    # Try to edit the message
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_admin_stats_keyboard()
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer("Statistika allaqachon yangi", show_alert=True)
        else:
            raise e

async def refresh_top_10_users(callback: CallbackQuery, db: Database):
    """Refresh and show top 10 referrers"""
    await callback.answer("🔄 Yangilanmoqda...")
    
    admin_service = AdminService(db)
    top_referrers = await admin_service.get_top_referrers(10)
    
    text = "🏆 <b>TOP 10 Referrerlar:</b>\n\n"
    
    if not top_referrers:
        text += "Hali referal yo'q"
    else:
        text += "<blockquote>"
        for i, user in enumerate(top_referrers, 1):
            username = user['username'] or "Noma'lum"
            first_name = user['full_name'].split()[0] if user['full_name'] else "Foydalanuvchi"
            text += f"{i}. {first_name} (@{username}) - {user['referral_count']} ta taklif\n"
        text += "</blockquote>"
        
    try:
        await callback.message.edit_text(
            text,
            reply_markup=get_top_referrers_keyboard()
        )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer("Ma'lumot allaqachon yangi", show_alert=True)
        else:
            raise e

async def close_message(callback: CallbackQuery):
    """Close/delete the current message"""
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception as e:
        logging.error(f"Failed to delete message: {e}")
        await callback.answer("Xabarni o'chirib bo'lmadi", show_alert=True)

async def export_user_data_message(callback: CallbackQuery, db: Database):
    """Export all user data to Excel"""
    await callback.message.answer("⏳ Exporting data...")
    
    admin_service = AdminService(db)
    file_path = await admin_service.export_users_data()
    
    if file_path:
        # Send file using FSInputFile
        document = FSInputFile(file_path, filename=os.path.basename(file_path))
        await callback.message.answer_document(
            document=document,
            caption=get_text('admin_export_success', 'uz')
        )
        
        # Clean up the file after sending
        try:
            os.remove(file_path)
        except:
            pass
    else:
        await callback.message.answer(get_text('admin_export_error', 'uz'))