from sqlalchemy import select, update

from apps.core.database.db import DataBase
from apps.core.database.db_repo.models.product_price import ProductPrice


class ProductPriceRepository:

    def __init__(self, db: DataBase):
        self.db = db


    async def get_by_product_and_country(self, product_id: str, country_code: str):
        async with self.db.get_session() as session:
            stmt = select(ProductPrice).where(
                ProductPrice.product_id == product_id,
                ProductPrice.country_code == country_code
            )
            result = await session.execute(stmt)
            return result.scalars().first()


    async def upsert_price(
            self,
            product_id: str,
            country_code: str,
            original_price: float,
            discounted_price: float,
            discounted_percentage: float,
            ru_price: float,
    ):
        async with self.db.get_session() as session:
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
                session.add(price)
            else:
                price.original_price = original_price
                price.discounted_price = discounted_price
                price.discounted_percentage = discounted_percentage
                price.ru_price = ru_price


    async def get_prices_by_product(self, product_id: str):
        """Получить все цены по товару"""
        async with self.db.get_session() as session:
            stmt = select(ProductPrice).where(ProductPrice.product_id == product_id)
            result = await session.execute(stmt)
            return result.scalars().all()


    async def update_ru_price(self, product_id: str, country_code: str, ru_price: float):
        """Обновить цену в рублях"""
        async with self.db.get_session() as session:
            stmt = (
                update(ProductPrice)
                .where(
                    ProductPrice.product_id == product_id,
                    ProductPrice.country_code == country_code
                )
                .values(ru_price=ru_price)
            )
            await session.execute(stmt)

