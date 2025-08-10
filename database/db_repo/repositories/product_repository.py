from sqlalchemy import select

from database.db import DataBase
from database.db_repo.models.product import Product


class ProductRepository:

    def __init__(self, db: DataBase):
        self.db = db


    async def get_by_product_id(self, product_id: str):
        async with self.db.get_session() as session:
            stmt = select(Product).where(Product.product_id == product_id)
            result = await session.execute(stmt)
            return result.scalars().first()


    async def add(self, product: Product):
        async with self.db.get_session() as session:
            await session.add(product)


    async def get_url_products(self) -> list[str]:
        async with self.db.get_session() as session:
            stmt = select(Product.url_product)
            result = await session.execute(stmt)
            return [row[0] for row in result.all()]



