from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import regions, regions_name


def parsing_price_keyboards():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Запустить парсер", callback_data="start_pars_price_product")],
            [InlineKeyboardButton(text="🏳️ Настройка регионов", callback_data="change_pars_product_regions")],
            [InlineKeyboardButton(text="Настройка формул", callback_data="formulas_setting")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="back_base_menu_keyboards")],
        ]
    )
    return keyboard


def back_parsing_price_keyboards():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪ Назад", callback_data="parsing_price_products")],
        ]
    )
    return keyboard


def formulas_keyboard(call_id: int) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for region in regions:
        button = InlineKeyboardButton(
            text=f'{regions_name.get(region)}',
            callback_data=f"new_formula:{region}:{call_id}"
        )
        inline_keyboard.append([button])
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        keyboard.inline_keyboard.extend(back_parsing_price_keyboards().inline_keyboard)

    return keyboard
