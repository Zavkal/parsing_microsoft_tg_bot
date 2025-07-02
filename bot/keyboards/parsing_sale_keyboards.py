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


def stop_parser_sale_keyboards():
    stop_parser_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⛔️ Остановить парсер распродаж", callback_data="stop_parser_sale")]
        ]
    )
    return stop_parser_keyboards_


def change_pars_county_sale_kb(regions: list, country: dict, regions_name: dict):
    inline_keyboard = []
    for region in regions:
        if country.get(region):  # Учитываем новое значение
            button = InlineKeyboardButton(
                text=f'✅ {regions_name.get(region)}',
                callback_data=f"change_pars_country:{region}"
            )
        else:
            button = InlineKeyboardButton(
                text=f'❌ {regions_name.get(region)}',
                callback_data=f"change_pars_country:{region}"
            )

        inline_keyboard.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    keyboard.inline_keyboard.extend(back_parsing_sale_keyboards().inline_keyboard)

    return keyboard









