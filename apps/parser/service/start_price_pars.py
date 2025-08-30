import asyncio
import time
from datetime import datetime, timedelta

from apps.parser.entities.parser_entity import ParserName
from apps.parser.handlers.parsing_price_products import pars_price
from config import ADMIN, regions_id, regions_name, moscow_tz, regions
from config_bot import repo_manager, bot


async def start_price_pars_products() -> None:
    start_time = time.time()
    links = await repo_manager.product_repo.get_url_products()
    country = await repo_manager.country_price_repo.get_all_county_pars_product()
    await bot.send_message(
        chat_id=ADMIN,
        text=f"Начат парсинг цен {len(links)} товаров.",
    )

    regions_to_parse = [region for region in regions if country.get(region)]
    # Создаем список задач
    tasks = [
        pars_price(links, country=regions_id.get(region))
        for region in regions_to_parse
    ]

    # Запускаем все запросы параллельно
    results = await asyncio.gather(*tasks)

    for (region, (old_links, new_links, exception)) in zip(regions_to_parse, results):
        if not country.get(region):
            continue  # Пропускаем регионы, которые не нужно парсить
        exception_text = "\n".join(exception)

        await bot.send_message(
            chat_id=ADMIN,
            text=(
                f'{regions_name.get(region)} собрано {len(old_links)} цен ✅\n'
                f'🎮 Новых товаров: {len(new_links)}\n'
                f'⚠️ Ошибок: {len(exception)}\n'
                f'{exception_text}'
            )
        )
    elapsed_time = int(time.time() - start_time)
    date = datetime.now(moscow_tz).strftime("%d-%m-%Y")
    await repo_manager.parser_schedule_repo.update_last_run(parser_name=ParserName.PARS_PRICE, date=date)
    await bot.send_message(
        chat_id=ADMIN,
        text=f'Работа завершена ✅\n'
             f'📅 Дата: {datetime.now(moscow_tz).strftime("%d-%m-%Y")}\n'
             f'⌛️ Время: {datetime.now(moscow_tz).strftime("%H:%M")}\n'
             f'⏰ Время парсинга: {str(timedelta(seconds=elapsed_time))[:-3]}',
    )
