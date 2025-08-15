from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def parsing_price_keyboards():
    parsing_price_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Запустить парсер", callback_data="start_pars_price_product")],
            [InlineKeyboardButton(text="🏳️ Настройка регионов", callback_data="change_pars_product_regions")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="back_base_menu_keyboards")],
        ]
    )
    return parsing_price_keyboards_


def back_parsing_price_keyboards():
    back_parsing_price_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪ Назад", callback_data="parsing_price_products")],
        ]
    )
    return back_parsing_price_keyboards_
