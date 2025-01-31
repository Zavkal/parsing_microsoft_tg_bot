from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def parsing_sale_keyboards():
    parsing_sale_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Запустить парсер", callback_data="start_parsing_sale")],
            [InlineKeyboardButton(text="🏳️ Настройка регионов", callback_data="change_pars_regions")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="sale_panel")],
        ]
    )
    return parsing_sale_keyboards_


def back_parsing_sale_keyboards():
    back_parsing_sale_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪ Назад", callback_data="parsing_sale")],
        ]
    )
    return back_parsing_sale_keyboards_















