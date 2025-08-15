import logging

from config_bot import repo_manager
from apps.parser.service.calculate import calculate_price
from apps.parser.handlers.parsing_products_from_links import pars_product_links
import json
import re
import aiohttp

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from apps.parser.service.fetch_for_parsing import fetch_for_price


async def pars_price(
        links: list,
        country: str,
        depth: int = 2,
        sale: bool = False,
) -> tuple[list, list, list]:

    if depth < 0:
        return [], [], []

    #  Отдельный парсер цен для Нигерии
    if country == "en-NG":
        driver = Driver(headless=False, disable_gpu=True)  # Запуск в фоновом режиме (без GUI)
        new_links = []
        old_links = []
        exception = []
        try:
            driver.get("https://www.microsoft.com/en-ng/store/deals/games/xbox")
            while True:
                game_cards = driver.find_elements(By.CLASS_NAME, "col")
                for card in game_cards:
                    # Извлекаем ссылку и название игры
                    link_elem = card.find_element(By.CSS_SELECTOR, "h3 a")
                    url = link_elem.get_attribute("href")
                    product_id = url.split("/")[-1].upper()
                    url = url.replace("www.microsoft.com/en-ng/p", "www.xbox.com/eu-EN/games/store")
                    url = url.replace(url.split("/")[-1], product_id)

                    if await repo_manager.product_repo.get_by_product_id(product_id=product_id):
                        old_links.append(url)
                        # Извлекаем цены
                        price_elements = card.find_elements(By.CSS_SELECTOR, "p[aria-hidden='true'] span")

                        if len(price_elements) >= 2:
                            orig_price_text = price_elements[0].text.strip()
                            sale_price_text = price_elements[1].text.strip()

                            # Форматируем цены
                            original_price = float(re.sub(r"[^\d.]", "", orig_price_text))
                            discounted_price = float(re.sub(r"[^\d.]", "", sale_price_text))
                            discounted_percentage = ((original_price - discounted_price) / original_price) * 100

                            # Округляем до 2 знаков после запятой
                            discounted_percentage = round(discounted_percentage, 2)
                            await repo_manager.product_price_repo.upsert_price(
                                country=country,
                                product_id=product_id,
                                original_price=original_price,
                                discounted_price=discounted_price,
                                discounted_percentage=discounted_percentage,
                                ru_price=float(await calculate_price(
                                    country[-2:],
                                    discounted_price,
                                    discounted_price)[1], )
                            )
                            if sale:
                                await repo_manager.product_repo.set_sale_status_for_product(product_id=product_id)
                            else:
                                await repo_manager.product_repo.remove_sale_status_for_product(product_id=product_id)

                    else:
                        new_links.append(url + '/001')

                try:
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Next')]"))
                    ).click()
                except TimeoutException:
                    break

        except Exception as e:
            logging.error(e)
            exception.append(e)

        finally:
            driver.quit()  # Закрываем браузер

        if new_links:
            await pars_product_links(new_links, "ru-RU")
            parsed_old, parsed_new, parsed_exceptions = await pars_price([], 'en-NG', depth=depth - 1, sale=sale)
            old_links += parsed_old
            new_links += parsed_new
            exception += parsed_exceptions

        return old_links, new_links, exception

    else:
        """Асинхронный парсер цен для одной страны."""
        new_links = []
        old_links = []
        exception = []

        async with aiohttp.ClientSession() as session:
            for link in links:
                link = link.replace(link.split('/')[3], country)
                product_id = link.split('/')[-2]

                if repo_manager.product_repo.get_by_product_id(product_id=product_id):
                    old_links.append(link)
                    html_content = await fetch_for_price(session=session,
                                                         url=link)

                    if html_content:
                        try:
                            pattern = r'window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});'
                            match = re.search(pattern, html_content, re.DOTALL)
                            if match:
                                preloaded_state = json.loads(match.group(1))
                                specific_prices = preloaded_state['core2']['products']['productSummaries'].get(
                                    product_id, {}).get('specificPrices', {}).get('purchaseable', [])

                                if specific_prices:
                                    original_price = specific_prices[0].get('msrp', 0)
                                    discounted_price = specific_prices[0].get('listPrice', 0)
                                    discounted_percentage = specific_prices[0].get('discountPercentage', 0)
                                    end_date_sale = specific_prices[0].get('endDate')
                                else:
                                    original_price = discounted_price = discounted_percentage = 0
                                    end_date_sale = None

                                await repo_manager.product_price_repo.upsert_price(
                                    country=country,
                                    product_id=product_id,
                                    original_price=original_price,
                                    discounted_price=discounted_price,
                                    discounted_percentage=discounted_percentage,
                                    ru_price=float(await calculate_price(
                                        country[-2:],
                                        discounted_price,
                                        discounted_price)[1],)
                                )

                                if sale:
                                    await repo_manager.product_repo.set_sale_status_for_product(product_id=product_id)
                                else:
                                    await repo_manager.product_repo.remove_sale_status_for_product(product_id=product_id)
                                await repo_manager.product_repo.update_end_date_sale_product(end_date_sale, product_id)
                        except Exception as e:
                            exception.append(f"Ошибка парсинга цены {product_id}, {link}, {e}")
                    else:
                        exception.append(f"Ошибка получения страницы {link}")

                else:
                    new_links.append(link)

        if new_links:
            await pars_product_links(new_links, "ru-RU")
            parsed_old, parsed_new, parsed_exceptions = await pars_price(new_links, country=country, depth=depth - 1,
                                                                         sale=sale)
            old_links += parsed_old
            new_links += parsed_new
            exception += parsed_exceptions

        return old_links, new_links, exception
