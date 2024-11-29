from aiogram import F, Bot
from aiogram import Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.types.input_file import FSInputFile
import logging

from config.settings import ADMINS
from src.utils.helpers import get_reports
from .keyboards import CustomKeyboards


router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return
    
    keyboard = CustomKeyboards.get_admin_panel()
    await message.answer(
        "Assalomu alaykum",
        reply_markup=keyboard
    )

@router.message(F.text == "Bugungi hisobotlarni qayta jo'natish")
async def reply(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        return
    
    await message.reply("Bugungi hisobotlar qayta tayyorlanyapti")
    
    
    report_files = get_reports()
    for file in report_files:
        try:
            photo = FSInputFile(file)
            await bot.send_photo(chat_id=user_id, photo=photo)
        except Exception as e:
            logging.error(f"Error sending pictures: {e}")



def register_handlers(dp: Dispatcher):
    dp.include_router(router)