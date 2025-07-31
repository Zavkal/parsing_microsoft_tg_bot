from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import DAYS_OF_WEEK_RU, FREQUENCY_RU


def auto_parsing_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Настройка авто парсинга", callback_data="settings_auto_parsing")],
            [InlineKeyboardButton(text="✅Вкл/❌Выкл", callback_data="2")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="base_auto_parsing")],
        ]
    )
    return keyboard


def back_auto_parsing_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪ Назад", callback_data="base_auto_parsing")],
        ]
    )
    return keyboard


def back_settings_auto_parsing_kb():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏪ Назад", callback_data="settings_auto_parsing")],
        ]
    )
    return keyboard


def generate_parser_settings_keyboard(config: dict, parser_name: str):
    freq = config.get("frequency")
    day_of_week = config.get("day_of_week")
    day_of_month = config.get("day_of_month")
    time = config.get("time")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"🕒 Частота: {FREQUENCY_RU.get(freq, '—')}",
                                  callback_data=f"edit_freq:{parser_name}")],
            [
                InlineKeyboardButton(
                    text=f"📅 День недели: {DAYS_OF_WEEK_RU.get(day_of_week, '—') if freq == 'weekly' else '—'}",
                    callback_data=f"edit_weekday:{parser_name}")
            ],
            [
                InlineKeyboardButton(text=f"📆 День месяца: {day_of_month if freq == 'monthly' else '—'}",
                                     callback_data=f"edit_monthday:{parser_name}")
            ],
            [InlineKeyboardButton(text=f"⏰ Время: {time or '—'}", callback_data=f"edit_time:{parser_name}")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="settings_auto_parsing")],
        ])

    return keyboard


def generate_frequency_keyboard(parser_name: str) -> InlineKeyboardMarkup:
    keyboard = []
    for key, value in FREQUENCY_RU.items():
        keyboard.append([InlineKeyboardButton(
            text=value,
            callback_data=f"set_freq:{parser_name}:{key}"
        )])
    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"settings_auto_parsing_edit:{parser_name}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def generate_day_of_week_keyboard(parser_name: str) -> InlineKeyboardMarkup:
    keyboard = []
    for eng_name, ru_name in DAYS_OF_WEEK_RU.items():
        keyboard.append([InlineKeyboardButton(text=ru_name,
            callback_data=f"set_weekday:{parser_name}:{eng_name}")])

    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"settings_auto_parsing_edit:{parser_name}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def generate_day_of_month_keyboard(parser_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for day in range(1, 32):
        builder.button(
            text=str(day),
            callback_data=f"set_monthday:{parser_name}:{day}"
        )
    builder.adjust(7)  # по 7 кнопок в ряд
    builder.button(text="🔙 Назад", callback_data=f"settings_auto_parsing_edit:{parser_name}")
    return builder.as_markup()
