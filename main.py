import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize bot and dispatcher with proper default properties
    bot = Bot(
        token=os.getenv('BOT_TOKEN'),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Initialize database
    from database.models import Database
    db = Database()
    await db.connect()
    
    # Add middleware
    from middleware.subscription import SubscriptionMiddleware
    dp.message.middleware(SubscriptionMiddleware(db))
    dp.callback_query.middleware(SubscriptionMiddleware(db))  
    dp.inline_query.middleware(SubscriptionMiddleware(db))  
    # Register routers
    from handlers.admin_handlers import admin_router
    from handlers.user_handlers import user_router
    dp.include_router(admin_router)
    dp.include_router(user_router)
    
    # Add database to context
    dp['db'] = db
    
    try:
        # Start polling
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
