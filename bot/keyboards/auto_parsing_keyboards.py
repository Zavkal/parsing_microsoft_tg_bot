from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def auto_parsing_keyboards():
    auto_parsing_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Настройка авто парсинга", callback_data="settings_auto_parsing")],
            [InlineKeyboardButton(text="❌ Выключить", callback_data="2")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="back_base_menu_keyboards")],
        ]
    )
    return auto_parsing_keyboards_


def settings_auto_parsing_keyboards():
    settings_auto_parsing_keyboards_ = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗓️ Настройка даты", callback_data="change_date_auto_parsing")],
            [InlineKeyboardButton(text="⏰ Настройка времени", callback_data="change_time_auto_parsing")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="base_auto_parsing")],
        ]
    )
    return settings_auto_parsing_keyboards_


