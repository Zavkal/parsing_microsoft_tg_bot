import asyncio
import logging

from bot.handlers.base_menu import router as start_router
from bot.handlers.sale import router as sale
from bot.handlers.parsing_sale import router as parsing_sale
from bot.handlers.auto_parsing import router as auto_parsing
from bot.handlers.get_data import router as get_data_file
from bot.handlers.big_parser import router as big_parser
from config_bot import dp, bot


async def main() -> None:
    logging.info("[Запуск бота] Бот запущен ассинхронно!")
    dp.include_routers(
        start_router,
        sale,
        parsing_sale,
        auto_parsing,
        get_data_file,
        big_parser,

    )
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())