import asyncio
import logging

from apps.bot.handlers.base_menu import router as start_router
from apps.bot.handlers.sale import router as sale
from apps.bot.handlers.parsing_sale import router as parsing_sale
from apps.bot.handlers.auto_parsing import router as auto_parsing
from apps.bot.handlers.get_data import router as get_data_file
from apps.bot.handlers.big_parser import router as big_parser
from apps.bot.handlers.parser_price import router as parser_price
from apps.bot.handlers.formulas_exchange_handler import router as formulas_exchange
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
        parser_price,
        formulas_exchange,
    )
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())