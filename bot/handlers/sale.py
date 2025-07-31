from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.keyboards.sale_keyboards import base_sale_keyboards
from database.db_bot import DataBase
from database.db_bot_repo.repositories.parser_schedule import ParserScheduleRepository
from operations.last_pars import get_last_pars

router = Router(name="Распродажи")


@router.callback_query(F.data == "sale_panel")
async def back_sale(callback_query: types.CallbackQuery, state: FSMContext, db: DataBase) -> None:
    await state.clear()
    repo_conf = ParserScheduleRepository(db)
    _,_, last_pars_date = await get_last_pars(repo_conf=repo_conf)
    await callback_query.message.edit_text(text=f"⌛️ Парсинг был: {last_pars_date}",
                                              reply_markup=base_sale_keyboards())







