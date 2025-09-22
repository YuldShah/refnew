from aiogram import Router, F, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.models import Database
from text.messages import get_text
from filters.user_filters import IsAdminFilter
from keyboards.admin_keyboards import admin_main_keyboard, get_main_menu_keyboard
from services.admin_service import AdminService
import os

# States for admin operations
class AdminStates(StatesGroup):
    waiting_for_user_id = State()

# Create admin menu router
admin_menu_router = Router()
admin_menu_router.message.filter(IsAdminFilter())

@admin_menu_router.message(F.text == "🏘 Main menu")
@admin_menu_router.message(F.text == "🏘 Bosh menyu")
@admin_menu_router.message(CommandStart())
async def admin_start_handler(message: Message, state: FSMContext):
    """Handle /start command for admins"""
    await state.clear()
    await show_admin_menu(message)

@admin_menu_router.message(Command("admin"))
async def admin_command(message: Message, state: FSMContext):
    """Handle /admin command to show admin panel"""
    await state.clear()
    await show_admin_menu(message)

async def show_admin_menu(message: Message):
    """Show main admin menu with options"""
    text = f"<b>{get_text('admin_panel', 'uz')}</b>"
    
    await message.answer(text, reply_markup=admin_main_keyboard('uz'))

# Message handlers for admin menu buttons
@admin_menu_router.message(F.text.in_([
    "📊 Ma'lumotlarni eksport qilish", "📊 Export user data",
    "📈 Statistika", "📈 Statistics",
    "🔐 Majburiy chatlar", "🔐 Manage Access"
]))
async def admin_menu_handler(message: Message, state: FSMContext, db: Database):
    """Handle admin menu button presses"""
    if message.text in ["📈 Statistika", "📈 Statistics"]:
        await message.reply(html.bold(f"📈 Stats menu"), reply_markup=get_main_menu_keyboard('uz'))
        await show_admin_stats_message(message, db)
    elif message.text in ["🔐 Majburiy chatlar", "🔐 Manage Access"]:
        await message.reply(html.bold(f"🔐 Manage Access menu"), reply_markup=get_main_menu_keyboard('uz'))
        # Initialize manage access with proper state
        from handlers.admin.manage_access import show_manage_access_menu as init_manage_access
        await init_manage_access(message, state)

async def show_top_referrers_message(message: Message, db: Database):
    """Show top 10 referrers"""
    admin_service = AdminService(db)
    top_referrers = await admin_service.get_top_referrers(10)
    
    text = get_text('admin_top_referrers_title', 'uz')
    
    if not top_referrers:
        text += "Hali referal yo'q"
    else:
        for i, user in enumerate(top_referrers, 1):
            username = user['username'] or "No username"
            text += get_text(
                'admin_top_referrer_item', 
                'uz', 
                position=i,
                full_name=user['full_name'],
                username=username,
                count=user['referral_count']
            ) + "\n"
    
    await message.answer(text)

async def user_lookup_request_message(message: Message, state: FSMContext):
    """Ask admin for user ID to lookup"""
    await state.set_state(AdminStates.waiting_for_user_id)
    await message.answer(get_text('admin_enter_user_id', 'uz'))

async def show_admin_stats_message(message: Message, db: Database):
    """Show admin statistics"""
    async with db.pool.acquire() as conn:
        total_users = await conn.fetchval('SELECT COUNT(*) FROM users WHERE telegram_id != 19')
        total_referrals = await conn.fetchval('''
            SELECT COUNT(*) FROM referrals r 
            JOIN users u1 ON r.referrer_id = u1.id 
            JOIN users u2 ON r.referred_id = u2.id 
            WHERE r.valid = TRUE AND u1.telegram_id != 19 AND u2.telegram_id != 19
        ''')
        pending_referrals = await conn.fetchval('''
            SELECT COUNT(*) FROM referrals r 
            JOIN users u1 ON r.referrer_id = u1.id 
            JOIN users u2 ON r.referred_id = u2.id 
            WHERE r.valid = FALSE AND u1.telegram_id != 19 AND u2.telegram_id != 19
        ''')
    
    # Get reward access count
    reward_access_count = await db.get_reward_access_count()
    
    text = f"📈 <b>Umumiy bot statistikasi: </b>\n"
    text += f"<blockquote>👥 Foydalanuvchilar: <b>{total_users}</b>\n"
    text += f"✅ Tasdiqlangan takliflar: <b>{total_referrals}</b>\n"
    text += f"⏳ Kutilayotgan takliflar: <b>{pending_referrals}</b>\n"
    text += f"🔓 Kirish huquqini olganlar: <b>{reward_access_count}</b></blockquote>"
    
    # Create inline keyboard for stats sub-menu
    from keyboards.admin_keyboards import get_admin_stats_keyboard
    await message.answer(text, reply_markup=get_admin_stats_keyboard('uz'))

async def show_manage_access_menu(message: Message):
    """Show manage access menu - now implemented!"""
    from handlers.admin.manage_access import show_manage_access_menu as show_access
    from aiogram.fsm.context import FSMContext
    
    # We need to get the FSMContext, but since it's not passed, we'll create a simple version
    text = "🔐 <b>Kirishni boshqarish</b>\n\n"
    text += "🎯 Bu bo'limda quyidagilarni boshqarish mumkin:\n\n"
    text += "📋 • Majburiy kanallar qo'shish/o'chirish\n"
    text += "👤 • Foydalanuvchilarga qo'lda ruxsat berish\n"
    text += "🚫 • Foydalanuvchilarni bloklash\n"
    text += "📊 • Kirish statistikasi\n\n"
    text += "⚠️ <i>To'liq funksional endi mavjud!</i>\n\n"
    text += "Davom etish uchun /admin buyrug'ini ishlating va 'Kirishni boshqarish' tugmasini bosing."
    
    await message.answer(text)

@admin_menu_router.message(AdminStates.waiting_for_user_id)
async def process_user_lookup(message: Message, state: FSMContext, db: Database):
    """Process user lookup by ID"""
    await state.clear()
    
    try:
        user_id = int(message.text.strip())
        admin_service = AdminService(db)
        user_info = await admin_service.get_user_by_telegram_id(user_id)
        
        if not user_info:
            await message.answer(get_text('admin_user_not_found', 'uz'))
            return
        
        # Format user info
        username = user_info.get('username') or "No username"
        text = get_text(
            'admin_user_info',
            'uz',
            telegram_id=user_info['telegram_id'],
            full_name=user_info['full_name'],
            username=username,
            referral_code=user_info['referral_code'],
            joined_at=user_info['joined_at'].strftime("%Y-%m-%d %H:%M:%S"),
            valid_referrals=user_info['valid_referrals'] or 0,
            pending_referrals=user_info['pending_referrals'] or 0
        )
        
        await message.answer(text)
        
    except ValueError:
        await message.answer(get_text('admin_user_not_found', 'uz'))

# Callback query handlers for admin stats inline buttons
