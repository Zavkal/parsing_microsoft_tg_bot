import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
import pytz

from bot.middleware.database import DBMiddleware
from database.db_bot import DataBase

# Указываем часовой пояс Москвы
moscow_tz = pytz.timezone("Europe/Moscow")

load_dotenv()
ADMIN = "1637636761"  # 763197387 585028070 1637636761
BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties())


dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = DataBase()
dp.message.middleware(DBMiddleware(db))
dp.callback_query.middleware(DBMiddleware(db))


regions = ["IN", "NG", "US", "AR", "TR", "UA"]

regions_id = {"IN": "en-IN",
              "NG": "en-NG",
              "US": "en-US",
              "AR": "es-AR",
              "TR": "tr-TR",
              "UA": "uk-UA"}

regions_name = {
        "IN": "🇪🇬 Египет",
        "NG": "🇳🇬 Нигерия",
        "US": "🇺🇸 Сша",
        "AR": "🇦🇷 Аргентина",
        "TR": "🇹🇷 Турция",
        "UA": "🇺🇦 Украина",
    }


main_game_list = [
    'https://www.xbox.com/eu-EN/games/browse?orderby=Title+Desc',
    'https://www.xbox.com/eu-EN/games/browse?orderby=Title+Asc'
]


product_pass = {
    'CFQ7TTC0QH5H': "UBISOFT+",
    'CFQ7TTC0K6L8': 'Xbox Game Pass Ultimate',
    'CFQ7TTC0KGQ8': 'PC Game Pass',
    'CFQ7TTC0P85B': 'Xbox Game Pass Standard',
    'CFQ7TTC0K5DJ': 'Xbox Game Pass Core',

}

logging.basicConfig(level=logging.INFO)