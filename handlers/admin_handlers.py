from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database.models import Database
from text.messages import get_text
from filters.user_filters import IsAdminFilter

admin_router = Router()
admin_router.message.filter(IsAdminFilter())
admin_router.callback_query.filter(IsAdminFilter())

@admin_router.message(CommandStart())
async def admin_start_handler(message: Message, state: FSMContext):
    await state.clear()
    await show_admin_menu(message)

@admin_router.message(Command('admin'))
async def admin_command_handler(message: Message, state: FSMContext):
    await state.clear()
    await show_admin_menu(message)

async def show_admin_menu(message: Message):
    text = f"<b>{get_text('admin_panel', 'uz')}</b>\n\n"
    text += "Statistika va boshqaruv paneli"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data='admin_stats')]
    ])
    await message.answer(text, reply_markup=keyboard)

@admin_router.callback_query(F.data == 'admin_stats')
async def admin_stats_handler(callback: CallbackQuery, db: Database):
    async with db.pool.acquire() as conn:
        total_users = await conn.fetchval('SELECT COUNT(*) FROM users')
        total_referrals = await conn.fetchval('SELECT COUNT(*) FROM referrals WHERE valid = TRUE')
        pending_referrals = await conn.fetchval('SELECT COUNT(*) FROM referrals WHERE valid = FALSE')
    
    text = f"📊 <b>Bot Statistikasi</b>\n\n"
    text += f"👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
    text += f"✅ Tasdiqlangan takliflar: <b>{total_referrals}</b>\n"
    text += f"⏳ Kutilayotgan takliflar: <b>{pending_referrals}</b>\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('back', 'uz'), callback_data='back_to_admin_menu')]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)

@admin_router.callback_query(F.data == 'back_to_admin_menu')
async def back_to_admin_menu_handler(callback: CallbackQuery):
    await show_admin_menu(callback.message)
