from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.keyboards.sale_keyboards import base_sale_keyboards
from database.db_bot import DataBase
from database.db_bot_repo.repositories.config import ConfigRepository

router = Router(name="Распродажи")


@router.callback_query(F.data == "sale_panel")
async def back_sale(callback_query: types.CallbackQuery, state: FSMContext, db: DataBase) -> None:
    await state.clear()
    repo_conf = ConfigRepository(db)
    last_pars_date = await repo_conf.get_config()
    await callback_query.message.edit_text(text=f"⌛️ Парсинг был: {last_pars_date['last_date_pars_sale']}",
                                              reply_markup=base_sale_keyboards())







