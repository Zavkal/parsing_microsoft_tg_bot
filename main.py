import asyncio

from bot.logger import logger
from bot.config import dp, bot
# from bot.middleware.authorization import AuthorizationMiddleware

from bot.handlers.base_menu import router as start_router
from bot.handlers.sale import router as sale
from bot.handlers.parsing_sale import router as parsing_sale
from bot.handlers.auto_parsing import router as auto_parsing

from database.db_bot import start_db


async def main() -> None:
    await start_db()
    logger.info("[Запуск бота] Бот запущен ассинхронно!")
    dp.include_routers(
        start_router,
        sale,
        parsing_sale,
        auto_parsing,

    )
    # dp.callback_query.middleware(AuthorizationMiddleware())
    # dp.message.middleware(AuthorizationMiddleware())
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())