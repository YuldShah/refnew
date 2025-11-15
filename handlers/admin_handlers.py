from aiogram import Router, F
from handlers.admin.admin_menu import admin_menu_router
from handlers.admin.manage_access import manage_access_router
from handlers.admin.admin_stats_router import admin_stats_router

# Create the main admin router
admin_router = Router()
# Filter to only handle private chats for admin commands
admin_router.message.filter(F.chat.type == "private")
admin_router.callback_query.filter(F.message.chat.type == "private")
admin_router.include_router(admin_menu_router)
admin_router.include_router(manage_access_router)
admin_router.include_router(admin_stats_router)
