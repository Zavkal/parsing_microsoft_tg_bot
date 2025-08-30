import asyncio
import logging

from apps.parser.handlers.parsing_links import open_page_and_scroll
from apps.parser.handlers.parsing_price_products import pars_price
from apps.parser.handlers.parsing_products_from_links import pars_product_links
from config import regions_id, ADMIN
from config_bot import bot


async def start_big_parser_products() -> None:
    links = []
    try:
        all_links_products = await open_page_and_scroll()
        links += all_links_products
    except Exception as e:
        logging.error(f"Произошла ошибка при работе драйвера: {e}")

        try:
            all_links_products = await open_page_and_scroll()
            links += all_links_products
        except Exception as e:
            logging.error(f"Произошла ошибка при работе драйвера 2 раз: {e}")

    await bot.send_message(
        chat_id=ADMIN,
        text=f"Найдено {len(links)}",
    )

    await pars_product_links(
        links=links,
        country='ru-RU',
    )

    tasks = [
        pars_price(
            links=links,
            country=regions_id.get("US"),
        )
    ]

    # Запускаем все запросы параллельно
    await asyncio.gather(*tasks)
