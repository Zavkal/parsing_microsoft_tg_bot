
from datetime import datetime

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from apps.bot.keyboards.big_parser_keyboards import products_menu_keyboards
from config import moscow_tz
from config_bot import repo_manager
from apps.parser.entities.parser_entity import ParserName
from apps.parser.service.last_pars import get_last_pars
from apps.parser.handlers.start_big_parser import start_big_parser_products

router = Router(name="Управление большим парсером")


@router.callback_query(F.data == "big_parser_products_menu")
async def products_menu(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    _, products, _ = await get_last_pars(repo_manager=repo_manager)
    await callback_query.message.edit_text(
        f"Парсинг был {products}",
        reply_markup=products_menu_keyboards()
    )


@router.callback_query(F.data == "start_big_parsing")
async def start_parser(callback_query: types.CallbackQuery) -> None:
    await callback_query.message.edit_text(
        "Парсер запущен"
    )

    await start_big_parser_products(callback_query)
    await callback_query.bot.send_message(chat_id=callback_query.from_user.id,
                                          text="Большой парсер окончил работу!")
    date = datetime.now(moscow_tz).strftime("%d-%m-%Y")
    await repo_manager.parser_schedule_repo.update_last_run(parser_name=ParserName.BIG_PARSER, date=date)

