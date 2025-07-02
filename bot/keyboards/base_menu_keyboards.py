from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def base_menu_keyboards():
    base_menu_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Распродажи", callback_data="sale_panel")],
            [InlineKeyboardButton(text="🎮 Товары ", callback_data="big_parser_products_menu")],
            [InlineKeyboardButton(text="💰 Цены", callback_data="parsing_price_products")],
            [InlineKeyboardButton(text="⏰ Авто парсинг", callback_data="base_auto_parsing")],
        ]
    )
    return base_menu_keyboards_


