import asyncio
import logging

import aiohttp
import requests
import json
import re

from aiogram import types

from config import DEVICE_MAPPING
from config_bot import repo_manager

from apps.parser.entities.parser_data_entity import ProductDataEntity
from apps.parser.service.fetch_for_parsing import fetch_for_product


async def pars_product_links(
        links: list,
        country: str,
        callback: types.CallbackQuery = None,
        pars_sale: bool = False,
) -> None:
    async with aiohttp.ClientSession() as session:
        counter = 0
        for link in links:
            counter += 1
            if counter % 100 == 0:
                if callback:
                    await callback.bot.send_message(chat_id=callback.from_user.id,
                                                text="Найдено 100 игр")
            capabilities_list = []
            link = link.replace(link.split('/')[3], country)
            try:
                # Отправляем GET-запрос
                response, response_text = await fetch_for_product(session=session,
                                                   url=link)

                product_id = link.split('/')[-2]

                all_data = ProductDataEntity(
                    product_id=product_id,
                    url_product=link.replace(link.split('/')[3], 'eu-EN'),
                    sale_product=pars_sale,
                )

                # Проверяем, успешен ли запрос
                if response.status != 200:
                    link = link.replace(link.split('/')[3], 'eu-EN')
                    response, response_text = await fetch_for_product(session=session,
                                                       url=link)
                if response.status == 200:

                    # Используем регулярное выражение для поиска данных, начиная с window.__PRELOADED_STATE__
                    pattern = r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});'
                    match = re.search(pattern, response_text, re.DOTALL)

                    if match:
                        preloaded_state = match.group(1)
                        preloaded_state_data = json.loads(preloaded_state)
                        try:
                            product_summary = preloaded_state_data['core2']['products']['productSummaries'][
                                f'{product_id}']
                            try:
                                product_dlc = \
                                preloaded_state_data['core2']['channels']['channelData'][f'WORKSWITH_{product_id}'][
                                    'data']['products'][0]['productId']
                            except Exception as e:  # noqa
                                product_dlc = ""
                            all_data.dlc = product_dlc
                            # Проверка языковой поддержки
                            languages_supported = product_summary.get('languagesSupported', {}).get('ru-RU', {})
                            all_data.audio_ru = languages_supported.get('isAudioSupported', False)
                            all_data.interface_ru = languages_supported.get('isInterfaceSupported', False)
                            all_data.subtitles_ru = languages_supported.get('areSubtitlesSupported', False)

                            # Название игры
                            all_data.game_name = product_summary.get('title')

                            # Видео
                            cms_videos = product_summary.get('cmsVideos')
                            all_data.link_video = cms_videos[0]['url'] if cms_videos else None

                            # Скриншоты
                            link_screenshot = product_summary.get('images', {}).get('screenshots', [])
                            # Извлекаем только URL-адреса из списка словарей
                            all_data.link_screenshot = ','.join(
                                item['url'] for item in link_screenshot if isinstance(item, dict) and 'url' in item)

                            all_data.image_url = product_summary.get('images', {}).get('boxArt', {}).get('url')

                            # Описание
                            description = product_summary.get('description')
                            if isinstance(description, str):
                                description = description.replace('\u00A0', ' ')
                                description = description.replace('\u202F', ' ')
                            else:
                                description = None
                            all_data.description = description

                            # Краткое описание
                            short_description = product_summary.get('shortDescription')
                            if isinstance(short_description, str):
                                short_description = short_description.replace('\u00A0', ' ')
                                short_description = short_description.replace('\u202F', ' ')
                            else:
                                short_description = None
                            all_data.short_description = short_description

                            # Разработчик и издатель
                            all_data.developer_name = product_summary.get('developerName')
                            all_data.publisher_name = product_summary.get('publisherName')

                            # Категории и возможности
                            all_data.category = ','.join(product_summary.get('categories'))
                            capabilities = product_summary.get('capabilities')
                            if capabilities:
                                for item in capabilities:
                                    capabilities_list.append(capabilities[item])
                            all_data.capabilities_list = ','.join(capabilities_list)

                            # Совместимость девайсов
                            try:
                                raw_devices = product_summary.get('availableOn', [])
                                device = ', '.join(DEVICE_MAPPING.get(d, d) for d in raw_devices)
                            except Exception as e:  # noqa
                                try:
                                    resp = requests.get(link.replace(link.split('/')[3], 'eu-EN'))
                                    match = re.search(pattern, resp.text, re.DOTALL)
                                    preloaded_state = match.group(1)
                                    preloaded_state_data = json.loads(preloaded_state)

                                    raw_devices = preloaded_state_data['core2']['products']['productSummaries'][
                                        product_id].get('availableOn', [])
                                    device = ', '.join(DEVICE_MAPPING.get(d, d) for d in raw_devices)
                                except Exception as e:  # noqa
                                    device = None
                            all_data.device = device

                            # Релиз
                            all_data.release_date = product_summary.get('releaseDate')

                            # Подписки и вес игры
                            all_data.pass_product_id = ','.join(product_summary.get('includedWithPassesProductIds'))
                            all_data.game_weight = (product_summary.get('maxInstallSize') / 1024 ** 3)

                            # Цены и скидки
                            specific_prices = product_summary.get('specificPrices', {}).get('purchaseable')
                            if len(specific_prices) > 0:
                                end_date_sale = specific_prices[0].get('endDate')
                            else:
                                end_date_sale = None
                            all_data.end_date_sale = end_date_sale
                            # Добавление продукта
                            await repo_manager.product_repo.upsert_product(product_data=all_data)
                        except json.JSONDecodeError:
                            logging.error(f"Ошибка парсинга JSON для продукта {product_id}")
                    else:
                        logging.error(f"Не удалось найти __PRELOADED_STATE__ в {link}")
                else:
                    logging.error(f"Не смог найти основную страницу на en-US {link}")
            except Exception as e:
                logging.error(f"Ошибка при обработке {link}: {e}")


if __name__ == '__main__':
    links = ["https://www.xbox.com/ru-RU/games/store/rain-world-downpour/9P0RMC2V6MTR/001"]
    country = "US"
    asyncio.run(pars_product_links(
        links=links,
        country=country,
    ))