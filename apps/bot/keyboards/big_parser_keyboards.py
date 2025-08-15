from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def products_menu_keyboards():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Запустить парсер", callback_data="start_big_parsing")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="back_base_menu_keyboards")],
        ]
    )
    return keyboard
