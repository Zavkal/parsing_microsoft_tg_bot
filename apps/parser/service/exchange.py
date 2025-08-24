import asyncio
from datetime import date

import aiohttp

from config_bot import repo_manager


async def get_new_exchange() -> None:
    rates_cb = await get_ru_centr_bank()
    date_exchange = date.today().strftime("%d-%m-%Y")
    usd_to_rub = get_rate_cb(rates=rates_cb, code='USD')
    try_to_rub = get_rate_cb(rates=rates_cb, code='TRY')  # Турция
    ngn_to_rub = get_rate_cb(rates=rates_cb, code='NGN')  # Наира Нигерия
    ars_to_rub = await get_ars()  # Песо Аргентины
    uah_to_rub = get_rate_cb(rates=rates_cb, code='UAH')  # Гривна Укр
    egp_to_rub = get_rate_cb(rates=rates_cb, code='EGP')  # Фунт Египет

    await repo_manager.exchange_repo.update_exchange(
        date_exchange=str(date_exchange),
        usd_to_rub=usd_to_rub,
        try_to_rub=try_to_rub,
        ngn_to_rub=ngn_to_rub,
        ars_to_rub=ars_to_rub,
        uah_to_rub=uah_to_rub,
        egp_to_rub=egp_to_rub,
    )


def get_rate_cb(rates: dict, code: str) -> float:
    val = rates.get(code)
    if not val:
        return -1
    return val["Value"] / val["Nominal"]


async def get_ru_centr_bank():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json(content_type=None)
            return data["Valute"]


async def get_ars():
    url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/ars.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return data["ars"]["rub"]



if __name__ == "__main__":
    asyncio.run(get_new_exchange())
