from aiogram.types import Message
from database.models import Database
from text.messages import get_text

async def show_rules(message: Message, db: Database):
    """Display bot rules to user"""
    
    # Placeholder rules text
    rules_text = get_text('rules_content', 'uz')
    
    await message.answer(rules_text)
