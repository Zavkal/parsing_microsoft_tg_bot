from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def base_sale_keyboards():
    base_menu_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="▶️ Парсер", callback_data="parsing_sale")],
            [InlineKeyboardButton(text="📑 Получить распродажу", callback_data="output_data_sale")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="back_base_menu_keyboards")],
        ]
    )
    return base_menu_keyboards_



















