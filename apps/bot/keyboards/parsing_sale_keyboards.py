from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def parsing_sale_keyboards():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Запустить парсер", callback_data="start_parsing_sale")],
            [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings_pars_sale")],
            [InlineKeyboardButton(text="📑 Получить распродажу", callback_data="output_data_sale")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="back_base_menu_keyboards")],
        ]
    )
    return keyboard


def parsing_sale_settings_kb(msg_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏳️ Настройка регионов", callback_data="change_pars_regions")],
            [InlineKeyboardButton(text="🔗 Добавить ссылку ", callback_data=f"add_link_for_pars:{msg_id}")],
            [InlineKeyboardButton(text="⛓️‍💥 Удалить ссылку ", callback_data=f"del_link_for_pars:{msg_id}")],
        ]
    )
    keyboard.inline_keyboard.extend(back_parsing_sale_keyboards().inline_keyboard)
    return keyboard


def back_parsing_sale_keyboards():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪ Назад", callback_data="sale_panel")],
        ]
    )
    return keyboard


def back_parsing_sale_settings_keyboards():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪ Назад", callback_data="settings_pars_sale")],
        ]
    )
    return keyboard


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
    keyboard.inline_keyboard.extend(back_parsing_sale_settings_keyboards().inline_keyboard)

    return keyboard









