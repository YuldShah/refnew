from aiogram import Router
from handlers.admin.admin_menu import admin_menu_router

# Create the main admin router
admin_router = Router()
admin_router.include_router(admin_menu_router)
