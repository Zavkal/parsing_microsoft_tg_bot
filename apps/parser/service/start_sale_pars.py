import asyncio
import logging
from datetime import datetime, timedelta
import time

from apps.parser.entities.parser_entity import ParserName
from apps.parser.handlers.parsing_links import open_page_and_scroll
from apps.parser.handlers.parsing_links_for_auto_pars import pars_link_for_auto_pars
from apps.parser.handlers.parsing_price_products import pars_price
from config import regions, regions_id, moscow_tz, ADMIN, regions_name
from config_bot import repo_manager, bot


async def start_sale_pars() -> None:
    start_time = time.time()
    sale_links = []
    links = await pars_link_for_auto_pars()
    links.extend(await repo_manager.link_yourself_repo.get_all_links_yourself())
    if len(links) > 0:
        text_response = f"⛓️‍💥 Найдено распродаж: {len(links)} ✅\n" + "\n".join(links)
        await bot.send_message(
            chat_id=ADMIN,
            text=text_response,
        )

        all_links_products = await open_page_and_scroll(links)
        sale_links += all_links_products
        country = await repo_manager.country_repo.get_all_county_pars_sale()
        await bot.send_message(chat_id=ADMIN,
                               text=f'⛓️‍💥 Найдено ссылок на игры: {len(sale_links)} ✅')
        regions_to_parse = [region for region in regions if country.get(region)]

        # Создаем список задач
        tasks = [
            pars_price(sale_links, country=regions_id.get(region))
            for region in regions_to_parse
        ]

        # Запускаем все запросы параллельно
        results = await asyncio.gather(*tasks)

        for (region, (old_links, new_links, exception)) in zip(regions_to_parse, results):
            if not country.get(region):
                continue  # Пропускаем регионы, которые не нужно парсить

            exception_text = "\n".join(exception)
            logging.error(exception_text)

            await bot.send_message(
                chat_id=ADMIN,
                text=(
                    f'{regions_name.get(region)} собрано {len(old_links)} цен ✅\n'
                    f'🎮 Новых товаров: {len(new_links)}\n'
                    f'⚠️ Ошибок: {len(exception)}\n'
                )
            )

        elapsed_time = int(time.time() - start_time)
        await bot.send_message(
            chat_id=ADMIN,
            text=f'Работа завершена ✅\n'
                 f'📅 Дата: {datetime.now(moscow_tz).strftime("%d-%m-%Y")}\n'
                 f'⌛️ Время: {datetime.now(moscow_tz).strftime("%H:%M")}\n'
                 f'⏰ Время парсинга: {str(timedelta(seconds=elapsed_time))[:-3]} ЧЧ:ММ',
        )

        # Необходимо все товары обнулить по sale_product
        await repo_manager.product_repo.set_sale_status_false_all_products()
        # Необходимо все айдишники обернуть в распродажу!
        product_ids = [link.split('/')[-2] for link in sale_links]
        await repo_manager.product_repo.set_sale_status_true_for_products(product_ids=product_ids)

    else:
        await bot.send_message(
            chat_id=ADMIN,
            text='Было найдено ровно 0 ссылок с распродажей :(',
        )

    date = datetime.now(moscow_tz).strftime("%d-%m-%Y")
    await repo_manager.parser_schedule_repo.update_last_run(parser_name=ParserName.SALE, date=date)
