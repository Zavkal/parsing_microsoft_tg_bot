import asyncio
import time
from datetime import datetime, timedelta

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.big_parser_keyboards import products_menu_keyboards
from bot.keyboards.pars_price_product_keyboards import parsing_price_keyboards, back_parsing_price_keyboards
from config import moscow_tz, regions, regions_name, regions_id
from database.db import get_url_products
from database.db_bot import DataBase
from database.db_bot_repo.repositories.country_price import CountyPriceRepository
from database.db_bot_repo.repositories.parser_schedule import ParserScheduleRepository
from entities.parser_entity import ParserName
from service.last_pars import get_last_pars
from parser.parsing_price_products import pars_price
from parser.start_big_parser import start_big_parser_products

router = Router(name="Управление большим парсером")


@router.callback_query(F.data == "big_parser_products_menu")
async def products_menu(callback_query: types.CallbackQuery, db: DataBase, state: FSMContext) -> None:
    repo_conf = ParserScheduleRepository(db)
    _, products, _ = await get_last_pars(repo_conf=repo_conf)
    await callback_query.message.edit_text(
        f"Парсинг был {products}",
        reply_markup=products_menu_keyboards()
    )


@router.callback_query(F.data == "start_big_parsing")
async def start_parser(callback_query: types.CallbackQuery, db: DataBase) -> None:
    repo_conf = ParserScheduleRepository(db)
    await callback_query.message.edit_text(
        "Парсер запущен"
    )

    await start_big_parser_products(callback_query)
    await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                          text=f"Большой парсер окончил работу!")
    date = datetime.now(moscow_tz).strftime("%d-%m-%Y")
    await repo_conf.update_last_run(parser_name=ParserName.BIG_PARSER, date=date)


# ---------------------------------------------------------------------------------------------------------------------
@router.callback_query(F.data == "parsing_price_products")
async def parsing_price_product(callback_query: types.CallbackQuery, state: FSMContext, db: DataBase) -> None:
    await state.clear()
    repo_country_price = CountyPriceRepository(db)
    country = await repo_country_price.get_all_county_pars_product()
    region_text = "Регионы для копирования цен:\n"
    for region in regions:
        if country.get(region):
            region_text += regions_name.get(region) + "\n"
    await callback_query.message.edit_text(text=region_text,
                                           reply_markup=parsing_price_keyboards())


@router.callback_query(F.data == "start_pars_price_product")
async def start_parsing_price_product(callback_query: types.CallbackQuery, state: FSMContext, db: DataBase) -> None:
    await state.clear()
    await callback_query.message.edit_text(
        "Парсер запущен",
    )
    await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                          text='✅Парсинг запущен.')
    start_time = time.time()
    links = get_url_products()
    repo_country_price = CountyPriceRepository(db)
    country = await repo_country_price.get_all_county_pars_product()
    await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                          text=f"Начат парсинг цен {len(links)} товаров.")

    regions_to_parse = [region for region in regions if country.get(region)]
    # Создаем список задач
    tasks = [
        pars_price(links, country=regions_id.get(region))
        for region in regions_to_parse
    ]

    # Запускаем все запросы параллельно
    results = await asyncio.gather(*tasks)

    for (region, (old_links, new_links, exception)) in zip(regions_to_parse, results):
        if not country.get(region):
            continue  # Пропускаем регионы, которые не нужно парсить
        exception_text = "\n".join(exception)

        await callback_query.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=(
                f'{regions_name.get(region)} собрано {len(old_links)} цен ✅\n'
                f'🎮 Новых товаров: {len(new_links)}\n'
                f'⚠️ Ошибок: {len(exception)}\n'
                f'{exception_text}'
            )
        )
    elapsed_time = int(time.time() - start_time)

    await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                          text=f'Работа завершена ✅\n'
                                               f'📅 Дата: {datetime.now(moscow_tz).strftime("%d-%m-%Y")}\n'
                                               f'⌛️ Время: {datetime.now(moscow_tz).strftime("%H:%M")}\n'
                                               f'⏰ Время парсинга: {str(timedelta(seconds=elapsed_time))[:-3]}')


@router.callback_query(F.data == "change_pars_product_regions")
async def start_parsing_price_product_(callback_query: types.CallbackQuery, state: FSMContext, db: DataBase) -> None:
    await state.clear()
    inline_keyboard = []
    repo_country_price = CountyPriceRepository(db)
    country = await repo_country_price.get_all_county_pars_product()
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
async def toggle_region_product_status(callback: types.CallbackQuery, db: DataBase, state: FSMContext) -> None:
    region = callback.data.split(":")[1]  # Получаем регион из callback_data
    repo_country_price = CountyPriceRepository(db)
    country = await repo_country_price.get_all_county_pars_product()

    # Инвертируем статус региона
    new_status = not country.get(region, 0)

    # Обновляем статус региона в БД
    await repo_country_price.update_region_pars_product(region, new_status)
    country = await repo_country_price.get_all_county_pars_product()
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




