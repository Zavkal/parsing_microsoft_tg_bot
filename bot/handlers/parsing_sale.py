from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import regions, regions_name
from bot.keyboards.parsing_sale_keyboards import parsing_sale_keyboards, back_parsing_sale_keyboards
from bot.keyboards.sale_keyboards import base_sale_keyboards
from database.db_bot import get_all_county_pars, update_region_pars

router = Router(name="Парсинг распродажи")


@router.callback_query(F.data == "parsing_sale")
async def parsing_sale_(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text(text=f"Регионы для копирования цен:"
                                                f"🇺🇸 Сша"
                                                f"🇳🇬 Нигерия"
                                                f"🇪🇬 Египет"
                                                f"🇦🇷 Аргентина"
                                                f"🇹🇷 Турция"
                                                f"🇺🇦 Украина",
                                              reply_markup=parsing_sale_keyboards())


@router.callback_query(F.data == "start_parsing_sale")
async def start_parsing_sale_(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()


@router.callback_query(F.data == "change_pars_regions")
async def start_parsing_sale_(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    inline_keyboard = []
    country = get_all_county_pars()
    for region in regions:
        if country.get(region):

            button = InlineKeyboardButton(
                text=f'✅ {regions_name.get(region)}',
                callback_data=f"change_pars_country:{region}"
                # Уникальный callback_data для каждой кнопки
            )
        else:
            button = InlineKeyboardButton(
                text=f'❌ {regions_name.get(region)}',
                callback_data=f"change_pars_country:{region}")

        inline_keyboard.append([button])
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    keyboard.inline_keyboard.extend(back_parsing_sale_keyboards().inline_keyboard)

    await callback_query.message.edit_text("Регионы для копирования цен:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("change_pars_country:"))
async def toggle_region_status(callback: types.CallbackQuery):
    region = callback.data.split(":")[1]  # Получаем регион из callback_data
    country = get_all_county_pars()

    # Инвертируем статус региона
    new_status = not country.get(region, 0)

    # Обновляем статус региона в БД
    update_region_pars(region, new_status)
    country = get_all_county_pars()
    # Обновляем клавиатуру
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
    await callback.message.edit_text("Выберите регионы:", reply_markup=keyboard)


@router.callback_query(F.data == "output_data_sale")
async def output_data_sale(callback_query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.edit_text(text=f"⌛️ Ручной парсинг был: 03.01.2025 в 15:30",
                                              reply_markup=base_sale_keyboards())


