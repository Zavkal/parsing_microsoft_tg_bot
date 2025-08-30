import asyncio
import time
from datetime import datetime, timedelta

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from apps.bot.keyboards.pars_price_product_keyboards import parsing_price_keyboards, back_parsing_price_keyboards
from apps.parser.entities.parser_entity import ParserName
from apps.parser.service.start_price_pars import start_price_pars_products
from config import moscow_tz, regions, regions_name, regions_id
from config_bot import repo_manager
from apps.parser.handlers.parsing_price_products import pars_price

router = Router(name="Управление парсером цен")


@router.callback_query(F.data == "parsing_price_products")
async def parsing_price_product(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    country = await repo_manager.country_price_repo.get_all_county_pars_product()
    region_text = "Регионы для копирования цен:\n"
    for region in regions:
        if country.get(region):
            region_text += regions_name.get(region) + "\n"
    await callback_query.message.edit_text(text=region_text,
                                           reply_markup=parsing_price_keyboards())


@router.callback_query(F.data == "start_pars_price_product")
async def start_parsing_price_product(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback_query.message.edit_text(
        "Парсер запущен",
    )
    await start_price_pars_products()



@router.callback_query(F.data == "change_pars_product_regions")
async def start_parsing_price_product_(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    inline_keyboard = []
    country = await repo_manager.country_price_repo.get_all_county_pars_product()
    for region in regions:
        if country.get(region):

            button = InlineKeyboardButton(
                text=f'✅ {regions_name.get(region)}',
                callback_data=f"change_pars_product_country:{region}"
                # Уникальный callback_data для каждой кнопки
            )
        else:
            button = InlineKeyboardButton(
                text=f'❌ {regions_name.get(region)}',
                callback_data=f"change_pars_product_country:{region}")

        inline_keyboard.append([button])
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    keyboard.inline_keyboard.extend(back_parsing_price_keyboards().inline_keyboard)

    await callback_query.message.edit_text("Регионы для копирования цен:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("change_pars_product_country:"))
async def toggle_region_product_status(callback: types.CallbackQuery, state: FSMContext) -> None:
    region = callback.data.split(":")[1]  # Получаем регион из callback_data
    country = await repo_manager.country_price_repo.get_all_county_pars_product()

    # Инвертируем статус региона
    new_status = not country.get(region, 0)

    # Обновляем статус региона в БД
    await repo_manager.country_price_repo.update_region_pars_product(region, new_status)
    country = await repo_manager.country_price_repo.get_all_county_pars_product()
    # Обновляем клавиатуру
    inline_keyboard = []
    for region in regions:
        if country.get(region):  # Учитываем новое значение
            button = InlineKeyboardButton(
                text=f'✅ {regions_name.get(region)}',
                callback_data=f"change_pars_product_country:{region}"
            )
        else:
            button = InlineKeyboardButton(
                text=f'❌ {regions_name.get(region)}',
                callback_data=f"change_pars_product_country:{region}"
            )

        inline_keyboard.append([button])

    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    keyboard.inline_keyboard.extend(back_parsing_price_keyboards().inline_keyboard)
    await callback.message.edit_text("Выберите регионы:", reply_markup=keyboard)