import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from bot.middleware.database import DBMiddleware
from database.db_bot import DataBase
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties())


dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = DataBase()
dp.message.middleware(DBMiddleware(db))
dp.callback_query.middleware(DBMiddleware(db))