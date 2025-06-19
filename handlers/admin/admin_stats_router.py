from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from filters.user_filters import IsAdminFilter
from handlers.admin.admin_stats import (
    show_admin_stats,
    show_top_10_users,
    search_user_request,
    process_user_search,
    export_user_data_message,
    refresh_admin_stats,
    refresh_top_10_users,
    close_message,
    AdminStatsStates
)
from text.messages import get_text

# Create admin stats router
admin_stats_router = Router()

# Apply admin filter to all handlers in this router
admin_stats_router.message.filter(IsAdminFilter())
admin_stats_router.callback_query.filter(IsAdminFilter())

@admin_stats_router.message(F.text.endswith("📊 Statistika"))
async def handle_admin_stats(message: Message, db):
    """Handle admin stats button"""
    await show_admin_stats(message, db)

@admin_stats_router.callback_query(F.data == 'admin_refresh_stats')
async def handle_refresh_admin_stats(callback: CallbackQuery, db):
    """Handle refresh admin stats"""
    await refresh_admin_stats(callback, db)

@admin_stats_router.callback_query(F.data == 'admin_top_10')
async def handle_admin_top_10(callback: CallbackQuery, db):
    """Handle admin top 10 referrers"""
    await show_top_10_users(callback, db)

@admin_stats_router.callback_query(F.data == 'admin_find_user')
async def handle_admin_find_user(callback: CallbackQuery, state: FSMContext):
    """Handle admin user search"""
    await search_user_request(callback, state)

@admin_stats_router.callback_query(F.data == 'admin_export')
async def handle_admin_export(callback: CallbackQuery, db):
    """Handle admin export data"""
    await export_user_data_message(callback, db)

@admin_stats_router.message(AdminStatsStates.waiting_for_search_user_id)
async def handle_admin_user_search(message: Message, state: FSMContext, db):
    """Handle admin user search input"""
    await process_user_search(message, state, db)

@admin_stats_router.callback_query(F.data == 'admin_refresh_top_10')
async def handle_refresh_admin_top_10(callback: CallbackQuery, db):
    """Handle refresh admin top 10 referrers"""
    await refresh_top_10_users(callback, db)

@admin_stats_router.callback_query(F.data == 'admin_close_message')
async def handle_close_message(callback: CallbackQuery):
    """Handle close message"""
    await close_message(callback)
