from aiogram.filters import BaseFilter
from aiogram.types import Message
import os

class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        admin_ids = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))
        return message.from_user.id in admin_ids

class IsUserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        admin_ids = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))
        return message.from_user.id not in admin_ids
