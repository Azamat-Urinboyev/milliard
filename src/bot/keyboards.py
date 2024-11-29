from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

class CustomKeyboards:
    @staticmethod
    def get_admin_panel():
        builder = ReplyKeyboardBuilder()

        buttons = [
            "Bugungi hisobotlarni qayta jo'natish"
        ]
        
        for button in buttons:
            builder.add(KeyboardButton(text=button))

        #The number of buttons in a row
        builder.adjust(2)

        return builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Select data type"
        )