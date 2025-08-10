import re

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.auto_parsing_keyboards import auto_parsing_kb, \
    generate_parser_settings_keyboard, generate_frequency_keyboard, generate_day_of_week_keyboard, \
    generate_day_of_month_keyboard, back_auto_parsing_kb, change_status_auto_pars_kb
from config import parsing_name
from config_bot import repo_manager
from service.generate_text_auto_pars import generate_text_auto_pars

router = Router(name="Автопарсинг")

class TimeInput(StatesGroup):
    waiting_for_time = State()


@router.callback_query(F.data == "base_auto_parsing")
async def base_auto_parsing(callback_query: types.CallbackQuery, state: FSMContext ):
    await state.clear()
    text = await generate_text_auto_pars(repo_manager)

    await callback_query.message.edit_text(text=text,
                                           reply_markup=auto_parsing_kb(),
                                           parse_mode='HTML')


@router.callback_query(F.data == "settings_auto_parsing")
async def settings_auto_parsing(callback_query: types.CallbackQuery, state: FSMContext ):
    conf_pars = await repo_manager.parser_schedule_repo.get_all_schedule_conditions()
    keyboard = []
    for parser in conf_pars.keys():
        data = conf_pars[parser]
        parser_name = data[0]['parser_name']
        keyboard.append([InlineKeyboardButton(
            text=f"⚙️ {parsing_name.get(parser_name)}",
            callback_data=f"settings_auto_parsing_edit:{parser_name}")])
    keyboard.extend(back_auto_parsing_kb().inline_keyboard)
    await state.clear()
    await callback_query.message.edit_text(text=f"⚙️ Настройка",
                                           reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))




@router.callback_query(F.data.startswith("settings_auto_parsing_edit:"))
async def parsing_sale_(callback_query: types.CallbackQuery, state: FSMContext ):
    pars_name = callback_query.data.split(":")[1]
    config = await repo_manager.parser_schedule_repo.get_schedule_by_parser(parser_name=pars_name)
    await state.clear()
    await callback_query.message.edit_text(text=f"⚙️ Настройка",
                                           reply_markup=generate_parser_settings_keyboard(config=config,
                                                                                          parser_name=pars_name))


@router.callback_query(F.data.startswith("edit_freq:"))
async def edit_frequency(callback: types.CallbackQuery):
    parser_name = callback.data.split(":")[1]
    await callback.message.edit_text(
        f"🔄 Выберите частоту запуска:",
        reply_markup=generate_frequency_keyboard(parser_name)
    )


@router.callback_query(F.data.startswith("edit_weekday:"))
async def edit_weekday(callback: types.CallbackQuery ):
    parser_name = callback.data.split(":")[1]

    config = await repo_manager.parser_schedule_repo.get_schedule_by_parser(parser_name)

    if config['frequency'] != 'weekly':
        await callback.answer("Доступно только при еженедельном режиме.", show_alert=True)
        return

    await callback.message.edit_text(
        f"📅 Выберите день недели:",
        reply_markup=generate_day_of_week_keyboard(parser_name)
    )


@router.callback_query(F.data.startswith("edit_monthday:"))
async def edit_monthday(callback: types.CallbackQuery ):
    parser_name = callback.data.split(":")[1]

    config = await repo_manager.parser_schedule_repo.get_schedule_by_parser(parser_name)

    if config['frequency'] != 'monthly':
        await callback.answer("Доступно только при ежемесячном режиме.", show_alert=True)
        return

    await callback.message.edit_text(
        f"📆 Выберите число месяца:",
        reply_markup=generate_day_of_month_keyboard(parser_name)
    )


@router.callback_query(F.data.startswith("edit_time:"))
async def edit_time(callback: types.CallbackQuery, state: FSMContext):
    parser_name = callback.data.split(":")[1]
    await state.set_state(TimeInput.waiting_for_time)
    msg_del = await callback.message.edit_text("⏰ Введите время в формате HH:MM (например, 14:30)")
    await state.update_data(parser_name=parser_name, msg_del=msg_del)


@router.message(TimeInput.waiting_for_time)
async def process_time_input(message: types.Message, state: FSMContext ):
    parser_name = (await state.get_data()).get("parser_name")
    msg_del = (await state.get_data()).get("msg_del")


    if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", message.text.strip()):
        await message.answer("❌ Неверный формат. Введите время в формате HH:MM, например 08:45.")
        await message.delete()
        return

    await repo_manager.parser_schedule_repo.update_parser_schedule(parser_name, time=message.text.strip())
    config = await repo_manager.parser_schedule_repo.get_schedule_by_parser(parser_name=parser_name)
    await state.clear()
    await message.answer(
        f"✅ Время обновлено.",
        reply_markup=generate_parser_settings_keyboard(config=config,
                                                       parser_name=parser_name)
    )
    await message.delete()
    await msg_del.delete()



@router.callback_query(F.data.startswith("set_freq:"))
async def set_frequency(callback: types.CallbackQuery ):
    _, parser_name, freq = callback.data.split(":")

    updates = {"frequency": freq}
    if freq == "daily":
        updates["day_of_week"] = None
        updates["day_of_month"] = None
    elif freq == "weekly":
        updates["day_of_month"] = None
    elif freq == "monthly":
        updates["day_of_week"] = None

    await repo_manager.parser_schedule_repo.update_parser_schedule(parser_name, **updates)
    config = await repo_manager.parser_schedule_repo.get_schedule_by_parser(parser_name=parser_name)
    await callback.message.edit_text(
        text=f"⚙️ Настройки: {parser_name}",
        reply_markup=generate_parser_settings_keyboard(config=config,
                                                       parser_name=parser_name,)
    )


@router.callback_query(F.data.startswith("set_weekday:"))
async def set_weekday(callback: types.CallbackQuery ):
    _, parser_name, day = callback.data.split(":")


    await repo_manager.parser_schedule_repo.update_parser_schedule(parser_name, day_of_week=day)
    config = await repo_manager.parser_schedule_repo.get_schedule_by_parser(parser_name=parser_name)
    await callback.message.edit_text(
        text=f"⚙️ Настройки: {parser_name}",
        reply_markup=generate_parser_settings_keyboard(config=config,
                                                       parser_name=parser_name,)
    )


@router.callback_query(F.data.startswith("set_monthday:"))
async def set_monthday(callback: types.CallbackQuery):
    _, parser_name, day = callback.data.split(":")


    await repo_manager.parser_schedule_repo.update_parser_schedule(parser_name, day_of_month=int(day))
    config = await repo_manager.parser_schedule_repo.get_schedule_by_parser(parser_name=parser_name)
    await callback.message.edit_text(
        text=f"⚙️ Настройки: {parser_name}",
        reply_markup=generate_parser_settings_keyboard(config=config,
                                                       parser_name=parser_name,)
    )


@router.callback_query(F.data == "change_status_auto_pars")
async def change_status_auto_pars(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    conf_repo = await repo_manager.parser_schedule_repo.get_all_schedule_conditions()

    await callback_query.message.edit_text(text="Управление парсерами:",
                                           reply_markup=change_status_auto_pars_kb(conf_pars=conf_repo))


@router.callback_query(F.data.startswith("change_pars_status:"))
async def change_pars_status(callback: types.CallbackQuery, state: FSMContext) -> None:
    parser_name = callback.data.split(":")[1]

    conf_repo = await repo_manager.parser_schedule_repo.get_all_schedule_conditions()

    # Инвертируем статус региона
    new_status = not conf_repo.get(parser_name)[0].get('is_enabled', 0)
    await repo_manager.parser_schedule_repo.update_status_pars(parser_name=parser_name,
                                  is_enabled=new_status)
    conf_repo = await repo_manager.parser_schedule_repo.get_all_schedule_conditions()

    await callback.message.edit_text(text="Управление парсерами:",
                                     reply_markup=change_status_auto_pars_kb(conf_pars=conf_repo))