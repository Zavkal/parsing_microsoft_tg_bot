from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_data_sale_files():
    #  Здесь будет функция создания кнопок на каждый файл
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Что-то получить в распродаже", callback_data="123")],
        ]
    )
    return kb


def get_data_sale_back_keyboards():
    get_data_sale_back_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪ Назад", callback_data="sale_panel")],
        ]
    )
    return get_data_sale_back_keyboards_













