import asyncio
import logging

# from bot.middleware.authorization import AuthorizationMiddleware

from bot.handlers.base_menu import router as start_router
from bot.handlers.sale import router as sale
from bot.handlers.parsing_sale import router as parsing_sale
from bot.handlers.auto_parsing import router as auto_parsing
from bot.handlers.get_data import router as get_data_file
from bot.handlers.big_parser import router as big_parser

from config import dp, bot

from database.db_bot import DataBase
from database.db import start_db as start_pars_db


async def main() -> None:
    db = DataBase()
    await db.start_db()
    start_pars_db()
    logging.info("[Запуск бота] Бот запущен ассинхронно!")
    dp.include_routers(
        start_router,
        sale,
        parsing_sale,
        auto_parsing,
        get_data_file,
        big_parser,

    )
    # dp.callback_query.middleware(AuthorizationMiddleware())
    # dp.message.middleware(AuthorizationMiddleware())
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())