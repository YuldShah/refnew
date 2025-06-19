from aiogram.filters import BaseFilter
from aiogram.types import Message
import os

class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            admin_ids_str = os.getenv('ADMIN_IDS', '')
            if not admin_ids_str:
                return False
            admin_ids = list(map(int, admin_ids_str.split(',')))
            return message.from_user.id in admin_ids
        except (ValueError, AttributeError):
            return False

class IsUserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            admin_ids_str = os.getenv('ADMIN_IDS', '')
            if not admin_ids_str:
                return True  # If no admins configured, everyone is a user
            admin_ids = list(map(int, admin_ids_str.split(',')))
            return message.from_user.id not in admin_ids
        except (ValueError, AttributeError):
            return True  # Default to user access if parsing fails
