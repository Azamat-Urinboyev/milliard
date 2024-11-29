import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types.input_file import FSInputFile
from aiogram.webhook.aiohttp_server import setup_application

from config.settings import BOT_TOKEN
from src.bot.handlers import register_handlers
from src.logging_config import setup_logging
from src.scheduler.scheduler_manager import SchedulerManager

from config.settings import GROUP_ID

async def main():
    setup_logging()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    scheduler = SchedulerManager(bot=bot)
    # await scheduler._sending_reports()
    scheduler.start()

    register_handlers(dp)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
    finally:
        await bot.session.close()

# Webhook alternative (for production deployment)
async def start_webhook(bot: Bot, dp: Dispatcher):
    # Set up webhook (replace with your webhook URL)
    WEBHOOK_URL = 'https://your-webhook-url.com/webhook'
    
    await bot.set_webhook(WEBHOOK_URL)
    
    # Setup aiohttp server for webhook
    app = setup_application(dp, bot)
    # Configure and run web server (example with aiohttp)
    # This is a placeholder and needs proper web server configuration

if __name__ == '__main__':
    asyncio.run(main())