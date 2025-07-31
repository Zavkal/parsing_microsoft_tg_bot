import asyncio
import logging
import re
import time
from datetime import datetime, timedelta
import pytz

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from bot.keyboards.base_menu_keyboards import del_msg_kb
from bot.keyboards.parsing_sale_keyboards import (parsing_sale_keyboards,
    stop_parser_sale_keyboards, change_pars_county_sale_kb, parsing_sale_settings_kb)
from config import regions, regions_name, regions_id
from database.db_bot import DataBase
from database.db_bot_repo.repositories.country import CountryRepository
from database.db_bot_repo.repositories.parser_schedule import ParserScheduleRepository
from entities.parser_entity import ParserName

from operations.parsing_links import open_page_and_scroll
from operations.parsing_links_for_auto_pars import pars_link_for_auto_pars
from operations.parsing_price_products import pars_price

router = Router(name="Парсинг распродажи")

moscow_tz = pytz.timezone("Europe/Moscow")


class NewLinkForPars(StatesGroup):
    new_link = State()


@router.callback_query(F.data == "parsing_sale")
async def parsing_sale_handler(callback_query: types.CallbackQuery, state: FSMContext, db: DataBase) -> None:
    await state.clear()
    repo_country = CountryRepository(db)
    country = await repo_country.get_all_county_pars()
    region_text = "Регионы для копирования цен:\n"
    for region in regions:
        if country.get(region):
            region_text += regions_name.get(region) + "\n"
    await callback_query.message.edit_text(text=region_text,
                                              reply_markup=parsing_sale_keyboards())


@router.callback_query(F.data == "start_parsing_sale")
async def start_parsing_sale_(callback_query: types.CallbackQuery, state: FSMContext, db: DataBase) -> None:
    await state.clear()
    await callback_query.message.edit_text(
        "✅ Парсер запущен",
        reply_markup=stop_parser_sale_keyboards()
    )
    await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                          text='✅ Парсер запущен.')
    start_time = time.time()
    sale_links = []
    links = await pars_link_for_auto_pars()
    links.append() # ВАЖНО добавить ссылку из ручного парса если есть (Придумай логику)
    if len(links) > 0:
        text_response = f"⛓️‍💥 Найдено распродаж: {len(links)} ✅\n" + "\n".join(links)
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                              text=text_response)

        all_links_products = await open_page_and_scroll(links)
        sale_links += all_links_products
        repo_country = CountryRepository(db)
        country = await repo_country.get_all_county_pars()
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                              text=f'⛓️‍💥 Найдено ссылок на игры: {len(sale_links)} ✅')

        regions_to_parse = [region for region in regions if country.get(region)]

        # Создаем список задач
        tasks = [
            pars_price(sale_links, country=regions_id.get(region), sale=True)
            for region in regions_to_parse
        ]

        # Запускаем все запросы параллельно
        results = await asyncio.gather(*tasks)

        for (region, (old_links, new_links, exception)) in zip(regions_to_parse, results):
            if not country.get(region):
                continue  # Пропускаем регионы, которые не нужно парсить

            exception_text = "\n".join(exception)
            logging.error(exception_text)

            await callback_query.bot.send_message(
                chat_id=callback_query.from_user.id,
                text=(
                    f'{regions_name.get(region)} собрано {len(old_links)} цен ✅\n'
                    f'🎮 Новых товаров: {len(new_links)}\n'
                    f'⚠️ Ошибок: {len(exception)}\n'
                )
            )

        elapsed_time = int(time.time() - start_time)
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                              text=f'Работа завершена ✅\n'
                                                   f'📅 Дата: {datetime.now(moscow_tz).strftime("%d-%m-%Y")}\n'
                                                   f'⌛️ Время: {datetime.now(moscow_tz).strftime("%H:%M")}\n'
                                                   f'⏰ Время парсинга: {str(timedelta(seconds=elapsed_time))[:-3]} ЧЧ:ММ')
    else:
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                              text=f'Было найдено ровно 0 ссылок с распродажей :(')

    date = datetime.now(moscow_tz).strftime("%d-%m-%Y")
    repo_conf = ParserScheduleRepository(db)
    await repo_conf.update_last_run(parser_name=ParserName.SALE, date=date)


@router.callback_query(F.data == "change_pars_regions")
async def start_parsing_sale_(callback_query: types.CallbackQuery, state: FSMContext, db: DataBase) -> None:
    await state.clear()
    repo_country = CountryRepository(db)
    country = await repo_country.get_all_county_pars()

    keyboard = change_pars_county_sale_kb(country=country, regions_name=regions_name, regions=regions)
    await callback_query.message.edit_text("Регионы для копирования цен:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("change_pars_country:"))
async def toggle_region_status(callback: types.CallbackQuery, db: DataBase, state: FSMContext) -> None:
    region = callback.data.split(":")[1]
    repo_country = CountryRepository(db)
    country = await repo_country.get_all_county_pars()

    # Инвертируем статус региона
    new_status = not country.get(region, 0)
    await repo_country.update_region_pars(region, new_status)
    country = await repo_country.get_all_county_pars()

    keyboard = change_pars_county_sale_kb(country=country, regions_name=regions_name, regions=regions)
    await callback.message.edit_text("Выберите регионы:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("settings_pars_sale"))
async def settings_pars_sale(callback: types.CallbackQuery, db: DataBase, state: FSMContext) -> None:
    repo_country = CountryRepository(db)
    country = await repo_country.get_all_county_pars()
    text = "Регионы для копирования цен:\n"
    for region in regions:
        if country.get(region):
            text += regions_name.get(region) + "\n"
    text+='\n\nСсылки:\n'
    await callback.message.edit_text(text=text,
                                     reply_markup=parsing_sale_settings_kb())


async def stop_parser_sale_products():
    pass


@router.callback_query(F.data == "stop_parser_sale")
async def stop_parser(callback_query: types.CallbackQuery) -> None:
    await stop_parser_sale_products()
    await callback_query.message.edit_text(
        "Парсер остановлен",
        reply_markup=parsing_sale_keyboards())


@router.callback_query(F.data == "add_link_for_pars")
async def add_link_for_pars(callback: types.CallbackQuery, state: FSMContext) -> None:
    call_del = await callback.message.answer(text='Введите ссылку с распродажами!')
    await state.update_data(call_del=call_del)
    await state.set_state(NewLinkForPars.new_link)


@router.message(NewLinkForPars.new_link)
async def add_link_for_pars_(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    call_del = data.get("call_del")
    link = message.text.strip()
    await message.delete()
    URL_REGEX = re.compile(
        r'^(https?://)?(www\.)?([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(/[\w\-._~:/?#[\]@!$&\'()*+,;=]*)?$'
    )
    if URL_REGEX.match(link):
        await call_del.edit_text(text=f"✅ Ссылка принята:\n{link}",
                                 reply_markup=del_msg_kb())
        await state.clear()
    else:
        msg_del = await message.answer("❌ Пожалуйста, введите корректную ссылку.")
        await asyncio.sleep(2)
        await msg_del.delete()



