from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.base_menu_keyboards import base_menu_keyboards
from database.db_bot import DataBase
from database.db_bot_repo.repositories.parser_schedule import ParserScheduleRepository
from service.last_pars import get_last_pars

router = Router(name="Автопарсинг")


@router.message(CommandStart())
async def command_start_handler(message: types.Message, db: DataBase, state: FSMContext) -> None:
    await state.clear()
    await message.delete()
    repo_conf = ParserScheduleRepository(db)
    new_products, products, sale_products = await get_last_pars(repo_conf=repo_conf)
    await message.bot.send_message(chat_id=message.chat.id,
                                   text=f"Последний парсинг был:\n"
                                        f"Новинки {new_products}\n"
                                        f"Вся база {products}\n"
                                        f"Распродажа {sale_products}\n",
                                   reply_markup=base_menu_keyboards())


@router.callback_query(F.data == "back_base_menu_keyboards")
async def command_start_handler(callback_query: types.CallbackQuery, db: DataBase, state: FSMContext) -> None:
    await state.clear()
    repo_conf = ParserScheduleRepository(db)
    new_products, products, sale_products = await get_last_pars(repo_conf=repo_conf)
    await callback_query.message.edit_text(text=f"Последний парсинг был:\n"
                                        f"Новинки {new_products}\n"
                                        f"Распродажа {sale_products}\n"
                                        f"Вся база {products}\n",

                                   reply_markup=base_menu_keyboards())


@router.callback_query(F.data == "del_message")
async def del_message_handler(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback_query.message.delete()