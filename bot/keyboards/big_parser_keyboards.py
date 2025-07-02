from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def products_menu_keyboards():
    products_menu_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Запустить парсер", callback_data="start_big_parsing")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="back_base_menu_keyboards")],
        ]
    )
    return products_menu_keyboards_


def stop_parser_keyboards():
    stop_parser_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⛔️ Остановить большой парсер", callback_data="stop_big_parser")]
        ]
    )
    return stop_parser_keyboards_


