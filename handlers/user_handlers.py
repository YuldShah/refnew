from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from database.models import Database
from text.messages import get_text, get_user_text
from filters.user_filters import IsUserFilter
from aiogram.exceptions import TelegramBadRequest
import os
import logging

user_router = Router()
user_router.message.filter(IsUserFilter())
user_router.callback_query.filter(IsUserFilter())

@user_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, db: Database):
    await state.clear()
    
    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name or ""
    
    # Check if user exists
    existing_user = await db.get_user(user_id)
    if existing_user:
        user_lang = await db.get_user_language(user_id)
        await message.answer(get_text('already_registered', user_lang))
        await show_main_menu(message, db)
        return
    
    # Handle referral
    referrer = None
    referral_code = None
    args = message.text.split()
    if len(args) > 1:
        referral_code = args[1]
        if len(referral_code) == 8:
            referrer = await db.get_user_by_referral_code(referral_code)
            if not referrer:
                await message.answer(get_text('invalid_referral', 'uz'))
                referral_code = None
            elif referrer['telegram_id'] == user_id:
                await message.answer(get_text('invalid_referral', 'uz'))
                referral_code = None
                referrer = None
        else:
            await message.answer(get_text('invalid_referral', 'uz'))
            referral_code = None
    
    # Add user
    success, user_referral_code = await db.add_user(user_id, username, full_name)
    
    if referrer and referral_code:
        await db.add_referral(referrer['telegram_id'], user_id, referral_code)
        user_lang = await db.get_user_language(user_id)
        await message.answer(get_text('referral_welcome', user_lang, referrer=referrer['full_name']))
        
        # Check if both users are subscribed to validate referral
        bot = message.bot
        channel_ids = db.get_mandatory_channel_ids()
        
        both_subscribed = True
        for channel_id in channel_ids:
            try:
                referrer_member = await bot.get_chat_member(channel_id, referrer['telegram_id'])
                user_member = await bot.get_chat_member(channel_id, user_id)
                
                if (referrer_member.status in ['left', 'kicked'] or 
                    user_member.status in ['left', 'kicked']):
                    both_subscribed = False
                    break
            except:
                both_subscribed = False
                break
        
        if both_subscribed:
            await db.validate_referral(referrer['telegram_id'], user_id)
    else:
        user_lang = await db.get_user_language(user_id)
        await message.answer(get_text('welcome', user_lang))
    
    await show_main_menu(message, db)

async def show_main_menu(message: Message, db: Database):
    user_lang = await db.get_user_language(message.from_user.id)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('referral_system', user_lang), callback_data='referral_system')],
        [InlineKeyboardButton(text=get_text('language_settings', user_lang), callback_data='language_settings')]
    ])
    await message.answer("<b>Menu</b>", reply_markup=keyboard)

@user_router.callback_query(F.data == 'language_settings')
async def language_settings_handler(callback: CallbackQuery, db: Database):
    user_id = callback.from_user.id
    user_lang = await db.get_user_language(user_id)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    
    if user_lang == 'uz':
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=get_text('switch_to_english', user_lang), callback_data='set_lang_en')
        ])
    else:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=get_text('switch_to_uzbek', user_lang), callback_data='set_lang_uz')
        ])
    
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=get_text('back', user_lang), callback_data='back_to_menu')
    ])
    
    text = f"{get_text('language_settings', user_lang)}\n\n{get_text('current_language', user_lang)}"
    
    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer()
        else:
            logging.error(f"Error in language_settings: {e}")

@user_router.callback_query(F.data.startswith('set_lang_'))
async def change_language_handler(callback: CallbackQuery, db: Database):
    user_id = callback.from_user.id
    new_lang = callback.data.split('_')[2]  # 'uz' or 'en'
    
    await db.update_user_language(user_id, new_lang)
    await callback.answer(get_text('language_changed', new_lang))
    
    try:
        await show_main_menu(callback.message, db)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass  # Already answered callback above
        else:
            logging.error(f"Error in change_language: {e}")

@user_router.callback_query(F.data == 'referral_system')
async def referral_system_handler(callback: CallbackQuery, db: Database):
    user_id = callback.from_user.id
    user_lang = await db.get_user_language(user_id)
    
    # Check unvalidated referrals and try to validate them
    unvalidated = await db.get_unvalidated_referrals(user_id)
    bot = callback.bot
    channel_ids = db.get_mandatory_channel_ids()
    
    for referral in unvalidated:
        both_subscribed = True
        try:
            for channel_id in channel_ids:
                referrer_member = await bot.get_chat_member(channel_id, user_id)
                referred_member = await bot.get_chat_member(channel_id, referral['referred_telegram_id'])
                
                if (referrer_member.status in ['left', 'kicked'] or 
                    referred_member.status in ['left', 'kicked']):
                    both_subscribed = False
                    break
            
            if both_subscribed:
                await db.validate_referral(user_id, referral['referred_telegram_id'])
        except:
            pass
    
    valid_count = await db.get_valid_referrals_count(user_id)
    pending_count = len(await db.get_unvalidated_referrals(user_id))
    
    bot_username = (await bot.get_me()).username
    user_data = await db.get_user(user_id)
    referral_link = f"https://t.me/{bot_username}?start={user_data['referral_code']}"
    
    text = f"{get_text('valid_referrals', user_lang, count=valid_count)}\n"
    text += f"{get_text('pending_referrals', user_lang, count=pending_count)}\n\n"
    text += get_text('your_referral_link', user_lang, link=referral_link)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text('back', user_lang), callback_data='back_to_menu')]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)

@user_router.callback_query(F.data == 'back_to_menu')
async def back_to_menu_handler(callback: CallbackQuery, db: Database):
    try:
        await show_main_menu(callback.message, db)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await callback.answer()
        else:
            logging.error(f"Error in back_to_menu: {e}")

@user_router.callback_query(F.data == 'check_subscription')
async def check_subscription_handler(callback: CallbackQuery, db: Database):
    user_lang = await db.get_user_language(callback.from_user.id)
    await callback.answer(get_text('not_subscribed', user_lang))
    await callback.answer(get_text('not_subscribed', user_lang))
