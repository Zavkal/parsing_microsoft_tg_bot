from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.base_menu_keyboards import base_menu_keyboards
from database.db_bot import DataBase
from database.db_bot_repo.repositories.config import ConfigRepository
from operations.last_pars import get_last_pars

router = Router(name="Добавление ссылок для парса")