from aiogram import types

from operations.parsing_links import open_page_and_scroll
from operations.parsing_products_for_links import pars_product_links


async def start_big_parser_products(callback: types.CallbackQuery):
    links = []
    try:
        all_links_products = await open_page_and_scroll()
        links += all_links_products
    except Exception as e:
        print(f"Произошла ошибка при работе драйвера: {e}")

        try:
            all_links_products = await open_page_and_scroll()
            links += all_links_products
        except Exception as e:
            print(f"Произошла ошибка при работе драйвера 2 раз: {e}")

    links = list(set(links))
    await callback.bot.send_message(chat_id=callback.from_user.id,
                                    text=f"Найдено {len(links)}")
    await pars_product_links(links=links, country='ru-RU', callback=callback)

