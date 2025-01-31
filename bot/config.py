import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv


load_dotenv()
ADMIN = "1637636761"  # 763197387 585028070 1637636761
BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties())


dp = Dispatcher(bot=bot, storage=MemoryStorage())



regions = ["IN", "NG", "US", "AR", "TR", "UA"]
regions_name = {
        "IN": "🇪🇬 Египет",
        "NG": "🇳🇬 Нигерия",
        "US": "🇺🇸 Сша",
        "AR": "🇦🇷 Аргентина",
        "TR": "🇹🇷 Турция",
        "UA": "🇺🇦 Украина",
    }




















