import asyncio
import logging
import re
import time
from datetime import datetime, timedelta
import pytz

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from apps.bot.keyboards.base_menu_keyboards import del_msg_kb, cancel_msg_kb
from apps.bot.keyboards.parsing_sale_keyboards import (change_pars_county_sale_kb,
                                                       parsing_sale_settings_kb)
from apps.bot.service.generate_text_settings import generate_text_pars_sale_settings
from config import regions, regions_name, regions_id
from config_bot import repo_manager
from apps.parser.entities.parser_entity import ParserName

from apps.parser.handlers.parsing_links import open_page_and_scroll
from apps.parser.handlers.parsing_links_for_auto_pars import pars_link_for_auto_pars
from apps.parser.handlers.parsing_price_products import pars_price

router = Router(name="Парсинг распродажи")

moscow_tz = pytz.timezone("Europe/Moscow")


class LinksForParsState(StatesGroup):
    new_link = State()
    del_link = State()


@router.callback_query(F.data == "start_parsing_sale")
async def start_parsing_sale_(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback_query.message.edit_text(
        "✅ Парсер запущен",
    )

    start_time = time.time()
    sale_links = []
    links = await pars_link_for_auto_pars()
    links.extend(await repo_manager.link_yourself_repo.get_all_links_yourself())
    if len(links) > 0:
        text_response = f"⛓️‍💥 Найдено распродаж: {len(links)} ✅\n" + "\n".join(links)
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                              text=text_response)

        all_links_products = await open_page_and_scroll(links)
        sale_links += all_links_products
        country = await repo_manager.country_repo.get_all_county_pars_sale()
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                              text=f'⛓️‍💥 Найдено ссылок на игры: {len(sale_links)} ✅')
        regions_to_parse = [region for region in regions if country.get(region)]

        # Создаем список задач
        tasks = [
            pars_price(sale_links, country=regions_id.get(region))
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

        # Необходимо все товары обнулить по sale_product
        await repo_manager.product_repo.set_sale_status_false_all_products()
        # Необходимо все айдишники обернуть в распродажу!
        product_ids = [link.split('/')[-2] for link in sale_links]
        await repo_manager.product_repo.set_sale_status_true_for_products(product_ids=product_ids)

    else:
        await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                              text='Было найдено ровно 0 ссылок с распродажей :(')

    date = datetime.now(moscow_tz).strftime("%d-%m-%Y")
    await repo_manager.parser_schedule_repo.update_last_run(parser_name=ParserName.SALE, date=date)


@router.callback_query(F.data == "change_pars_regions")
async def change_pars_regions(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    country = await repo_manager.country_repo.get_all_county_pars_sale()

    keyboard = change_pars_county_sale_kb(country=country, regions_name=regions_name, regions=regions)
    await callback_query.message.edit_text("Регионы для копирования цен:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("change_pars_country:"))
async def toggle_region_status(callback: types.CallbackQuery, state: FSMContext) -> None:
    region = callback.data.split(":")[1]

    country = await repo_manager.country_repo.get_all_county_pars_sale()

    # Инвертируем статус региона
    new_status = not country.get(region, 0)
    await repo_manager.country_repo.update_region_pars(region, new_status)
    country = await repo_manager.country_repo.get_all_county_pars_sale()

    keyboard = change_pars_county_sale_kb(country=country, regions_name=regions_name, regions=regions)
    await callback.message.edit_text("Выберите регионы:", reply_markup=keyboard)


@router.callback_query(F.data == "settings_pars_sale")
async def settings_pars_sale(callback: types.CallbackQuery, state: FSMContext) -> None:
    text = await generate_text_pars_sale_settings()
    await callback.message.edit_text(text=text,
                             reply_markup=parsing_sale_settings_kb(msg_id=callback.message.message_id),
                             disable_web_page_preview=True,
                             )


@router.callback_query(F.data.startswith("add_link_for_pars"))
async def add_link_for_pars(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg_id = callback.data.split(":")[1]
    await callback.answer()
    call_del = await callback.message.answer(
        text='Введите ссылку с распродажами!',
        reply_markup=cancel_msg_kb())
    await state.update_data(call_del=call_del, msg_id=msg_id)
    await state.set_state(LinksForParsState.new_link)


@router.message(LinksForParsState.new_link)
async def add_link_for_pars_(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    call_del = data.get("call_del")
    msg_id = int(data.get("msg_id"))
    link = message.text.strip()

    await message.delete()

    URL_REGEX = re.compile(
        r'^(https?://)?(www\.)?([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}(/[\w\-._~:/?#[\]@!$&\'()*+,;=]*)?$'
    )
    all_links = await repo_manager.link_yourself_repo.get_all_links_yourself()

    if URL_REGEX.match(link):
        if link in all_links:
            msg_del = await message.answer("❌ Данная ссылка уже есть!")
            await asyncio.sleep(2)
            await msg_del.delete()
        else:
            await call_del.edit_text(text=f"✅ Ссылка принята:\n{link}",
                                     reply_markup=del_msg_kb())
            await repo_manager.link_yourself_repo.create_new_link_yourself(url=link)
            text = await generate_text_pars_sale_settings()
            await message.bot.edit_message_text(
                chat_id=message.from_user.id,
                message_id=msg_id,
                text=text,
                reply_markup=parsing_sale_settings_kb(msg_id=msg_id),
                disable_web_page_preview=True,

            )
            await state.clear()
    else:
        msg_del = await message.answer("❌ Пожалуйста, введите корректную ссылку.")
        await asyncio.sleep(2)
        await msg_del.delete()


@router.callback_query(F.data.startswith("del_link_for_pars"))
async def del_link_for_pars(callback: types.CallbackQuery, state: FSMContext) -> None:
    msg_id = callback.data.split(":")[1]
    await callback.answer()
    call_del = await callback.message.answer(
        text='Введите ссылку для удаления!',
        reply_markup=cancel_msg_kb())
    await state.update_data(call_del=call_del, msg_id=msg_id)
    await state.set_state(LinksForParsState.del_link)


@router.message(LinksForParsState.del_link)
async def del_link_for_pars_(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    call_del = data.get("call_del")
    msg_id = int(data.get("msg_id"))
    link = message.text.strip()
    await message.delete()
    all_links = await repo_manager.link_yourself_repo.get_all_links_yourself()
    if link in all_links:
        await call_del.edit_text(text=f"✅ Ссылка удалена:\n{link}",
                                 reply_markup=del_msg_kb())
        await repo_manager.link_yourself_repo.delete_link_yourself(url=link)
        text = await generate_text_pars_sale_settings()
        await message.bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=msg_id,
            text=text,
            reply_markup=parsing_sale_settings_kb(msg_id=msg_id),
            disable_web_page_preview=True,
        )
        await state.clear()
    else:
        msg_del = await message.answer("❌ Пожалуйста, введите корректную ссылку.")
        await asyncio.sleep(2)
        await msg_del.delete()