import pytest

from apps.parser.service.calculate import calculate_price

@pytest.mark.asyncio
async def test_calculate_price() -> None:
    country_code: str = "IN"
    original_price: float = 2.2
    discounted_price: float = 1.1

    await calculate_price(
        country_code=country_code,
        original_price=original_price,
        discounted_price=discounted_price,
    )
