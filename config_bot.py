import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from apps.app.database.db import DataBase as DataBase_db
from apps.app.database.db_bot import DataBase as DataBase_db_bot

from dotenv import load_dotenv

from apps.app.database.repositories_manager import RepoManager

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties())
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_BOT_URL = os.getenv("DATABASE_BOT_URL")

dp = Dispatcher(bot=bot, storage=MemoryStorage())

db = DataBase_db(DATABASE_URL)
db_bot = DataBase_db_bot(DATABASE_BOT_URL)

repo_manager = RepoManager(
    db=db,
    db_bot=db_bot
)
