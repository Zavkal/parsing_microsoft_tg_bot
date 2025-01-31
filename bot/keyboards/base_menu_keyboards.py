from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def base_menu_keyboards():
    base_menu_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Распродажи", callback_data="sale_panel")],
            [InlineKeyboardButton(text="🎮 Игры ", callback_data="2")],
            [InlineKeyboardButton(text="🗃️ Dlc ", callback_data="2")],
            [InlineKeyboardButton(text="💰 Валюта", callback_data="2")],
            [InlineKeyboardButton(text="⏰ Авто парсинг", callback_data="base_auto_parsing")],
            [InlineKeyboardButton(text="📑 Получить файлы", callback_data="2")],
        ]
    )
    return base_menu_keyboards_


