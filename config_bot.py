import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from database.db import DataBase as DataBase_db
from database.db_bot import DataBase as DataBase_db_bot

from dotenv import load_dotenv

from database.repositories_manager import RepoManager

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties())
db_url = os.getenv("DATABASE_URL")
db_bot_url = os.getenv("DATABASE_BOT_URL")

dp = Dispatcher(bot=bot, storage=MemoryStorage())

db = DataBase_db(db_url)
db_bot = DataBase_db_bot(db_bot_url)

repo_manager = RepoManager(
    db=db,
    db_bot=db_bot
)
