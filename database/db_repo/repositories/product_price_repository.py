from sqlalchemy import select

from database.db_repo.models.product_price_model import ProductPrice


class ProductPriceRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_product_and_country(self, product_id: str, country_code: str):
        stmt = select(ProductPrice).where(
            ProductPrice.product_id == product_id,
            ProductPrice.country_code == country_code
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def upsert_price(self, product_id: str, country_code: str,
                           original_price: float, discounted_price: float,
                           discounted_percentage: float, ru_price: float):
        price = await self.get_by_product_and_country(product_id, country_code)
        if not price:
            price = ProductPrice(
                product_id=product_id,
                country_code=country_code,
                original_price=original_price,
                discounted_price=discounted_price,
                discounted_percentage=discounted_percentage,
                ru_price=ru_price
            )
            self.session.add(price)
        else:
            price.original_price = original_price
            price.discounted_price = discounted_price
            price.discounted_percentage = discounted_percentage
            price.ru_price = ru_price
