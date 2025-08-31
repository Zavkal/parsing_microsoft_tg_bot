# Ограничитель для одновременных запросов (например, не более 3 запросов одновременно)
import asyncio
import logging

SEMAPHORE = asyncio.Semaphore(3)


async def fetch_for_price(session, url) -> str | None:
    """Асинхронный запрос с ограничением числа одновременных запросов"""
    async with SEMAPHORE:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            logging.error(f"Ошибка запроса {url}: {e}")
    return None


async def fetch_for_product(session, url):
    """Асинхронный запрос с ограничением числа одновременных запросов"""
    async with SEMAPHORE:
        async with session.get(url) as response:
            return response, await response.text()