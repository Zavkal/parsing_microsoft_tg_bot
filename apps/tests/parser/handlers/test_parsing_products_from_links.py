import pytest

from apps.parser.handlers.parsing_products_from_links import pars_product_links


@pytest.mark.asyncio
async def test_pars_product_links():
    links = ["https://www.xbox.com/ru-RU/games/store/rain-world-downpour/9P0RMC2V6MTR/001"]
    country = "US"
    await pars_product_links(
        links=links,
        country=country,
    )
    assert country == "US"