import asyncio

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from apps.bot.keyboards.base_menu_keyboards import cancel_msg_kb
from apps.bot.keyboards.pars_price_product_keyboards import formulas_keyboard
from apps.bot.service.generate_text_fromulas import generate_text_formulas_settings
from config_bot import repo_manager

router = Router(name="Управление формулами")


class NewFormulas(StatesGroup):
    formula = State()


@router.callback_query(F.data == "formulas_setting")
async def formulas_setting(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = await generate_text_formulas_settings(repo_manager=repo_manager)
    await callback_query.message.edit_text(
        text=text,
        reply_markup=formulas_keyboard(call_id=callback_query.message.message_id),
    )


@router.callback_query(F.data.startswith("new_formula:"))
async def new_formula(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await callback_query.answer()
    data = callback_query.data.split(":")[1:]
    country_code = data[0]
    call_id = data[1]
    msg_del = await callback_query.message.answer(text=('Введите формулу!\n'
                                                        'В самом начале всегда представляй цену.\n'
                                                        'Пример:ЦЕНА *0.9 + 200\n'
                                                        'Мы пишем только *0.9 + 200'),
                                                  reply_markup=cancel_msg_kb())

    await state.update_data(country_code=country_code, msg_del=msg_del, call_id=call_id)
    await state.set_state(NewFormulas.formula)


@router.message(NewFormulas.formula)
async def add_link_for_pars_(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()
    country_code = data["country_code"]
    msg_del = data["msg_del"]
    call_id = data["call_id"]
    await msg_del.delete()
    formula = message.text.strip()

    validate = "0123456789/*-+ ."

    for symbol in formula:
        if symbol not in validate:
            msg_del = await message.answer(text='Вводить можно только цифры и операнды /*-+')
            await asyncio.sleep(2)
            await msg_del.delete()
            return

    await repo_manager.formulas_repo.update_formulas(
        country_name=country_code,
        formula=formula,
    )



    text = await generate_text_formulas_settings(repo_manager=repo_manager)

    await message.bot.edit_message_text(text=text,
                                        reply_markup=formulas_keyboard(call_id=call_id))
    await state.clear()
