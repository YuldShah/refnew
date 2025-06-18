from aiogram.types import Message
from database.models import Database
from text.messages import get_text

async def show_rewards(message: Message, db: Database):
    """Display available rewards to user"""
    
    # Placeholder reward text
    reward_text = get_text('reward_content', 'uz')
    
    await message.answer(reward_text)
