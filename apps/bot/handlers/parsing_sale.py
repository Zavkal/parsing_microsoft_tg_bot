import asyncio
import re

import pytz

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from apps.bot.keyboards.base_menu_keyboards import del_msg_kb, cancel_msg_kb
from apps.bot.keyboards.parsing_sale_keyboards import (change_pars_county_sale_kb,
                                                       parsing_sale_settings_kb)
from apps.bot.service.generate_text_settings import generate_text_pars_sale_settings
from apps.parser.service.start_sale_pars import start_sale_pars
from config import regions, regions_name
from config_bot import repo_manager


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
    await start_sale_pars()


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