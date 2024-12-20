import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import setup_application, WebhookRequestHandler
import aiohttp
from aiohttp import web

from config.settings import BOT_TOKEN
from src.bot.handlers import register_handlers
from src.logging_config import setup_logging
from src.scheduler.scheduler_manager import SchedulerManager

WEB_SERVER_HOST
WEB_SERVER_PORT

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "my-secret"
BASE_WEBHOOK_URL = "https://aiogram.dev"


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)



async def main():
    setup_logging()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    scheduler = SchedulerManager(bot=bot)
    scheduler.start()

    register_handlers(dp)
    
    try:
        # Use webhook for production
        await start_webhook(bot, dp)
    except Exception as e:
        logging.error(f"Error starting webhook: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())