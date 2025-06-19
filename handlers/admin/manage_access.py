import re
import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest
from database.models import Database
from text.messages import get_text
from keyboards.admin_keyboards import (
    get_manage_access_keyboard,
    get_mandatory_channels_keyboard,
    get_manual_access_keyboard,
    get_confirm_keyboard,
    admin_main_keyboard
)
from filters.user_filters import IsAdminFilter

# States for manage access operations
class ManageAccessStates(StatesGroup):
    main_menu = State()
    mandatory_channels = State()
    add_channel_title = State()
    add_channel_link = State()
    confirm_add_channel = State()
    confirm_delete_channel = State()
    manual_access = State()
    add_user_access = State()
    remove_user_access = State()

# Create manage access router
manage_access_router = Router()
manage_access_router.message.filter(IsAdminFilter())
manage_access_router.callback_query.filter(IsAdminFilter())

async def show_manage_access_menu(message: Message, state: FSMContext):
    """Show main manage access menu"""
    # Send menu change notification
    
    await state.set_state(ManageAccessStates.main_menu)
    
    text = "Quyidagi amalardan birini tanlang:"
    
    await message.answer(text, reply_markup=get_manage_access_keyboard('uz'))

@manage_access_router.callback_query(F.data == "mandatory_channels", ManageAccessStates.main_menu)
async def show_mandatory_channels(callback: CallbackQuery, state: FSMContext, db: Database):
    """Show mandatory channels management"""
    await state.set_state(ManageAccessStates.mandatory_channels)
    
    channels = await db.get_mandatory_channels()
    
    text = "📋 <b>Majburiy kanallar</b>\n\n"
    text += "Bot avtomatik ravishda quyidagi barcha kanallarga a'zo bo'lgan foydalanuvchilarga ruxsat beradi.\n\n"
    
    if not channels:
        text = "📋 <b>Majburiy kanallar</b>\n\nHozircha majburiy kanallar yo'q. Foydalanuvchilar botdan foydalanish uchun qo'shilishi kerak bo'lgan kanallarni qo'shing."
    
    await callback.message.edit_text(text, reply_markup=get_mandatory_channels_keyboard('uz', channels))

@manage_access_router.callback_query(F.data == "back_to_access", ManageAccessStates.mandatory_channels)
async def back_to_access_menu(callback: CallbackQuery, state: FSMContext):
    """Back to main access menu"""
    await state.set_state(ManageAccessStates.main_menu)
    
    text = "🔐 <b>Kirishni boshqarish</b>\n\n"
    text += "Quyidagi amalardan birini tanlang:"
    
    await callback.message.edit_text(text, reply_markup=get_manage_access_keyboard('uz'))

@manage_access_router.callback_query(F.data == "add_mandatory_channel", ManageAccessStates.mandatory_channels)
async def add_channel_request_title(callback: CallbackQuery, state: FSMContext):
    """Request channel title"""
    await state.set_state(ManageAccessStates.add_channel_title)
    
    text = "📝 <b>Kanal qo'shish</b>\n\n"
    text += "Qo'shmoqchi bo'lgan kanalning nomini yuboring:"
    
    await callback.message.edit_text(text)
    await callback.answer()

@manage_access_router.message(ManageAccessStates.add_channel_title)
async def process_channel_title(message: Message, state: FSMContext):
    """Process channel title and request link"""
    await state.update_data(title=message.text)
    await state.set_state(ManageAccessStates.add_channel_link)
    
    text = "🔗 <b>Kanal havolasi</b>\n\n"
    text += "Kanalning havolasini quyidagi formatlardan birida yuboring:\n\n"
    text += "• Username: <code>kanalnom</code>\n"
    text += "• @ bilan username: <code>@kanalnom</code>\n"
    text += "• Ochiq havola: <code>https://t.me/kanalnom</code>\n\n"
    text += "<i>Yoki kanaldan xabar forward qiling (maxfiy kanallar uchun yaxshiroq)</i>"
    
    await message.answer(text)

@manage_access_router.message(ManageAccessStates.add_channel_link)
async def process_channel_link(message: Message, state: FSMContext, db: Database):
    """Process channel link and confirm"""
    USERNAME_PATTERN = r"^[a-zA-Z][\w\d_]{4,31}$"
    AT_USERNAME_PATTERN = r"^@[a-zA-Z][\w\d_]{4,31}$"  
    PUBLIC_LINK_PATTERN = r"^https://t\.me/[a-zA-Z][\w\d_]{4,31}$"
    
    chat_id = None
    link = None
    
    if message.forward_from_chat:
        chat_id = message.forward_from_chat.id
        if message.forward_from_chat.username:
            link = f"https://t.me/{message.forward_from_chat.username}"
        else:
            try:
                invite_link = await message.bot.create_chat_invite_link(
                    chat_id=chat_id, 
                    name=f"Join link by bot"
                )
                link = invite_link.invite_link
            except Exception as e:
                await message.answer("❌ Botni kanalga admin qilib qo'shing va qayta urinib ko'ring")
                return
    else:
        text = message.text
        username = None
        
        if re.match(USERNAME_PATTERN, text):
            username = f"@{text}"
            link = f"https://t.me/{text}"
        elif re.match(AT_USERNAME_PATTERN, text):
            username = text
            link = f"https://t.me/{text[1:]}"
        elif re.match(PUBLIC_LINK_PATTERN, text):
            username = f"@{text[13:]}"
            link = text
        else:
            await message.answer("❌ Noto'g'ri format. Iltimos, to'g'ri formatda yuboring.")
            return
        
        try:
            chat = await message.bot.get_chat(username)
            chat_id = chat.id
        except:
            await message.answer("❌ Kanal topilmadi. Kanal mavjud va bot admin ekanligini tekshiring.")
            return
    
    # Get channel info for confirmation
    try:
        channel_info = await message.bot.get_chat(chat_id)
        member_count = await message.bot.get_chat_member_count(chat_id)
        bot_member = await message.bot.get_chat_member(chat_id, message.bot.id)
    except Exception as e:
        await message.answer("❌ Botni kanalga admin qilib qo'shing va qayta urinib ko'ring")
        return
    
    data = await state.get_data()
    title = data.get("title")
    
    await state.update_data(chat_id=chat_id, link=link)
    await state.set_state(ManageAccessStates.confirm_add_channel)
    
    text = f"✅ <b>Tasdiqlash</b>\n\n"
    text += f"<b>Kanal ma'lumotlari:</b>\n"
    text += f"📝 Nom: <b>{channel_info.title}</b>\n"
    text += f"👥 A'zolar soni: <b>{member_count}</b>\n"
    text += f"📄 Tavsif: <blockquote>{channel_info.description or 'Tavsif yo\'q'}</blockquote>\n\n"
    text += "Kanalni majburiy kanallar ro'yxatiga qo'shishni tasdiqlaysizmi?"
    
    await message.answer(text, reply_markup=get_confirm_keyboard('uz'))

@manage_access_router.callback_query(F.data == "confirm", ManageAccessStates.confirm_add_channel)
async def confirm_add_channel(callback: CallbackQuery, state: FSMContext, db: Database):
    """Confirm adding channel"""
    data = await state.get_data()
    chat_id = data.get("chat_id")
    title = data.get("title")
    link = data.get("link")
    
    # Check if channel already exists
    channels = await db.get_mandatory_channels()
    if any(ch['chat_id'] == chat_id for ch in channels):
        await callback.answer("⚠️ Bu kanal allaqachon qo'shilgan")
        return
    
    # Add channel to database
    success = await db.add_mandatory_channel(chat_id, title, link)
    
    if success:
        await callback.answer("✅ Kanal muvaffaqiyatli qo'shildi")
        await state.set_state(ManageAccessStates.mandatory_channels)
        
        # Show updated channels list
        channels = await db.get_mandatory_channels()
        text = "📋 <b>Majburiy kanallar</b>\n\n"
        text += "Bot avtomatik ravishda BARCHA quyidagi kanallarga a'zo bo'lgan foydalanuvchilarga ruxsat beradi.\n\n"
        
        
        await callback.message.edit_text(text, reply_markup=get_mandatory_channels_keyboard('uz', channels))
    else:
        await callback.answer("❌ Kanalni qo'shishda xatolik yuz berdi")

@manage_access_router.callback_query(F.data == "cancel", ManageAccessStates.confirm_add_channel)
async def cancel_add_channel(callback: CallbackQuery, state: FSMContext, db: Database):
    """Cancel adding channel"""
    await callback.answer("❌ Bekor qilindi")
    await state.set_state(ManageAccessStates.mandatory_channels)
    
    channels = await db.get_mandatory_channels()
    text = "📋 <b>Majburiy kanallar</b>\n\n"
    text += "Bot avtomatik ravishda BARCHA quyidagi kanallarga a'zo bo'lgan foydalanuvchilarga ruxsat beradi.\n\n"
    
    if not channels:
        text += "Hozircha majburiy kanallar yo'q."
    
    await callback.message.edit_text(text, reply_markup=get_mandatory_channels_keyboard('uz', channels))

@manage_access_router.callback_query(F.data.startswith("delete_channel_"))
async def confirm_delete_channel(callback: CallbackQuery, state: FSMContext, db: Database):
    """Confirm channel deletion"""
    chat_id = int(callback.data.split("_")[2])
    
    channels = await db.get_mandatory_channels()
    channel = next((ch for ch in channels if ch['chat_id'] == chat_id), None)
    
    if not channel:
        await callback.answer("❌ Kanal topilmadi")
        return
    
    await state.update_data(delete_chat_id=chat_id)
    await state.set_state(ManageAccessStates.confirm_delete_channel)
    
    text = f"⚠️ <b>O'chirishni tasdiqlash</b>\n\n"
    text += f"'{channel['title']}' kanalini o'chirishni tasdiqlaysizmi?\n\n"
    text += "<i>Bu amalni bekor qilib bo'lmaydi.</i>"
    
    await callback.message.edit_text(text, reply_markup=get_confirm_keyboard('uz'))

@manage_access_router.callback_query(F.data == "confirm", ManageAccessStates.confirm_delete_channel)
async def delete_channel_confirmed(callback: CallbackQuery, state: FSMContext, db: Database):
    """Delete channel confirmed"""
    data = await state.get_data()
    chat_id = data.get("delete_chat_id")
    
    success = await db.remove_mandatory_channel(chat_id)
    
    if success:
        await callback.answer("✅ Kanal o'chirildi")
    else:
        await callback.answer("❌ Kanalni o'chirishda xatolik")
    
    await state.set_state(ManageAccessStates.mandatory_channels)
    
    # Show updated channels list
    channels = await db.get_mandatory_channels()
    text = "📋 <b>Majburiy kanallar</b>\n\n"
    text += "Bot avtomatik ravishda BARCHA quyidagi kanallarga a'zo bo'lgan foydalanuvchilarga ruxsat beradi.\n\n"
    
    if not channels:
        text += "Hozircha majburiy kanallar yo'q."
    
    await callback.message.edit_text(text, reply_markup=get_mandatory_channels_keyboard('uz', channels))

@manage_access_router.callback_query(F.data == "cancel", ManageAccessStates.confirm_delete_channel)
async def cancel_delete_channel(callback: CallbackQuery, state: FSMContext, db: Database):
    """Cancel channel deletion"""
    await callback.answer("❌ Bekor qilindi")
    await state.set_state(ManageAccessStates.mandatory_channels)
    
    channels = await db.get_mandatory_channels()
    text = "📋 <b>Majburiy kanallar</b>\n\n"
    text += "Bot avtomatik ravishda BARCHA quyidagi kanallarga a'zo bo'lgan foydalanuvchilarga ruxsat beradi.\n\n"
    
    if not channels:
        text += "Hozircha majburiy kanallar yo'q."
    
    await callback.message.edit_text(text, reply_markup=get_mandatory_channels_keyboard('uz', channels))

@manage_access_router.callback_query(F.data == "reset_all_channels", ManageAccessStates.mandatory_channels)
async def reset_all_channels_confirm(callback: CallbackQuery, state: FSMContext):
    """Confirm reset all channels"""
    await state.set_state(ManageAccessStates.confirm_delete_channel)
    await state.update_data(reset_all=True)
    
    text = "⚠️ <b>BARCHA kanallarni o'chirish</b>\n\n"
    text += "BARCHA majburiy kanallarni o'chirishni tasdiqlaysizmi?\n\n"
    text += "<b>Bu amalni bekor qilib bo'lmaydi!</b>"
    
    await callback.message.edit_text(text, reply_markup=get_confirm_keyboard('uz'))

# Continue with manual access management...
@manage_access_router.callback_query(F.data == "manual_access", ManageAccessStates.main_menu)
async def show_manual_access(callback: CallbackQuery, state: FSMContext):
    """Show manual access management"""
    await state.set_state(ManageAccessStates.manual_access)
    
    text = "👤 <b>Qo'lda kirish boshqaruvi</b>\n\n"
    text += "Bu yerda foydalanuvchilarga qo'lda ruxsat berish yoki olib qo'yish mumkin."
    
    await callback.message.edit_text(text, reply_markup=get_manual_access_keyboard('uz'))

@manage_access_router.callback_query(F.data == "add_user_access", ManageAccessStates.manual_access)
async def add_user_access_request(callback: CallbackQuery, state: FSMContext):
    """Request user for adding access"""
    await state.set_state(ManageAccessStates.add_user_access)
    
    text = "✅ <b>Foydalanuvchiga ruxsat berish</b>\n\n"
    text += "Ruxsat bermoqchi bo'lgan foydalanuvchining xabarini forward qiling yoki uning ID raqamini yuboring.\n\n"
    text += "Masalan: <code>123456789</code>"
    
    await callback.message.edit_text(text)
    await callback.answer()

@manage_access_router.message(ManageAccessStates.add_user_access)
async def process_add_user_access(message: Message, state: FSMContext, db: Database):
    """Process adding user access"""
    if message.forward_from:
        user_id = message.forward_from.id
        mention = message.forward_from.mention_html()
        username = message.forward_from.username
    elif message.text.isnumeric():
        user_id = int(message.text)
        mention = f"<a href='tg://user?id={user_id}'>{user_id}</a>"
        username = None
    else:
        await message.answer("❌ Forward qilingan xabar yoki to'g'ri ID raqam yuboring")
        return
    
    # Check if user exists
    user = await db.get_user(user_id)
    
    if user:
        # User exists, grant manual access
        success = await db.set_manual_access(user_id, 1)
        if success:
            await message.answer(f"✅ {mention} foydalanuvchiga qo'lda ruxsat berildi.\n\nFoydalanuvchi majburiy kanallarga a'zo bo'lmasdan ham botdan foydalana oladi.")
        else:
            await message.answer("❌ Ruxsat berishda xatolik yuz berdi")
    else:
        # Create user with manual access
        success = await db.create_user_with_manual_access(user_id, 1)
        if success:
            await message.answer(f"✅ {mention} foydalanuvchiga qo'lda ruxsat berildi.")
        else:
            await message.answer("❌ Foydalanuvchi yaratishda xatolik yuz berdi")
    
    await state.set_state(ManageAccessStates.manual_access)
    
    text = "👤 <b>Qo'lda kirish boshqaruvi</b>\n\n"
    text += "Bu yerda foydalanuvchilarga qo'lda ruxsat berish yoki olib qo'yish mumkin."
    
    await message.answer(text, reply_markup=get_manual_access_keyboard('uz'))

@manage_access_router.callback_query(F.data == "remove_user_access", ManageAccessStates.manual_access)
async def remove_user_access_request(callback: CallbackQuery, state: FSMContext):
    """Request user for removing access"""
    await state.set_state(ManageAccessStates.remove_user_access)
    
    text = "❌ <b>Foydalanuvchidan ruxsatni olib qo'yish</b>\n\n"
    text += "Ruxsatni olib qo'ymoqchi bo'lgan foydalanuvchining xabarini forward qiling yoki uning ID raqamini yuboring.\n\n"
    text += "Masalan: <code>123456789</code>"
    
    await callback.message.edit_text(text)
    await callback.answer()

@manage_access_router.message(ManageAccessStates.remove_user_access)
async def process_remove_user_access(message: Message, state: FSMContext, db: Database):
    """Process removing user access"""
    if message.forward_from:
        user_id = message.forward_from.id
        mention = message.forward_from.mention_html()
    elif message.text.isnumeric():
        user_id = int(message.text)
        mention = f"<a href='tg://user?id={user_id}'>{user_id}</a>"
    else:
        await message.answer("❌ Forward qilingan xabar yoki to'g'ri ID raqam yuboring")
        return
    
    user = await db.get_user(user_id)
    
    if user:
        # User exists, deny access
        success = await db.set_manual_access(user_id, -1)
        if success:
            await message.answer(f"❌ {mention} foydalanuvchisidan ruxsat olib qo'yildi.")
        else:
            await message.answer("❌ Ruxsatni olib qo'yishda xatolik yuz berdi")
    else:
        # Create user with denied access
        success = await db.create_user_with_manual_access(user_id, -1)
        if success:
            await message.answer(f"❌ {mention} foydalanuvchisiga kirish taqiqlandi.")
        else:
            await message.answer("❌ Foydalanuvchi yaratishda xatolik yuz berdi")
    
    await state.set_state(ManageAccessStates.manual_access)
    
    text = "👤 <b>Qo'lda kirish boshqaruvi</b>\n\n"
    text += "Bu yerda foydalanuvchilarga qo'lda ruxsat berish yoki olib qo'yish mumkin."
    
    await message.answer(text, reply_markup=get_manual_access_keyboard('uz'))

@manage_access_router.callback_query(F.data == "back_to_access", ManageAccessStates.manual_access)
async def back_to_access_from_manual(callback: CallbackQuery, state: FSMContext):
    """Back to main access menu from manual access"""
    await state.set_state(ManageAccessStates.main_menu)
    
    text = "🔐 <b>Kirishni boshqarish</b>\n\n"
    text += "Quyidagi amalardan birini tanlang:"
    
    await callback.message.edit_text(text, reply_markup=get_manage_access_keyboard('uz'))
