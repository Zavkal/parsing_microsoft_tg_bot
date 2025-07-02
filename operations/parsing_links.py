import re
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumbase import Driver
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from config import main_game_list


async def open_page_and_scroll(links: list = main_game_list):
    """Открывает страницу, скроллит до конца и извлекает ссылки на продукты."""
    all_link_products = []

    async def process_link(link):
        """Обрабатывает отдельную страницу."""
        driver = Driver(headless=True,
                        chromium_arg=["--disable-gpu", "--disable-software-rasterizer", "--disable-webgl"]
                        )
        try:
            await asyncio.to_thread(driver.get, link)  # Открываем страницу
            await asyncio.sleep(2)  # Ждем загрузки

            while True:
                try:
                    load_more_button = await asyncio.to_thread(
                        WebDriverWait(driver, 5).until,
                        EC.visibility_of_element_located((By.XPATH, '//button[contains(@aria-label, "Load more")]'))
                    )
                    if load_more_button.is_displayed():
                        await asyncio.to_thread(load_more_button.click)  # Клик по кнопке
                        await asyncio.sleep(2)  # Ждем загрузки новых элементов
                    else:
                        break
                except (NoSuchElementException, TimeoutException):
                    break  # Если кнопки нет, выходим

            links = await get_product_links(driver)
            return links

        finally:
            await asyncio.to_thread(driver.quit)  # Безопасное закрытие драйвера

    # Запускаем обработку всех ссылок параллельно
    if links == main_game_list:
        results = []
        for link in links:
            result = await process_link(link.replace(link.split('/')[3], 'en-US'))
            if result:
                results.append(result)
    else:
        results = await asyncio.gather(*(process_link(link.replace(link.split('/')[3], 'en-US')) for link in links))

    # Объединяем все ссылки из результатов
    for result in results:
        if result:
            all_link_products.extend(result)

    return list(set(all_link_products))  # Убираем дубликаты


async def get_product_links(driver):
    """Извлекает ссылки на продукты со страницы."""
    links = []
    try:
        product_containers = await asyncio.to_thread(
            driver.find_elements,
            By.XPATH, '//div[contains(@class,"ProductCard-module__cardWrapper___")]'
        )

        for container in product_containers:
            try:
                html_content = await asyncio.to_thread(container.get_attribute, 'outerHTML')
                extracted_links = re.findall(r'href=["\'](.*?)["\']', html_content)
                links.extend(extracted_links)
            except Exception as e:
                print(f"Ошибка при извлечении ссылки: {e}")

        return links

    except Exception as e:
        print(f'ФАТАЛЬНАЯ ОШИБКА РАБОТЫ: {e}')
        return []  # Возвращаем пустой список при ошибке
