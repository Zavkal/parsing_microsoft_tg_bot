from sqlalchemy import select

from database.db_repo.models.product_model import Product


class ProductRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_product_id(self, product_id: str):
        stmt = select(Product).where(Product.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def add(self, product: Product):
        self.session.add(product)

    async def update_audio(self, product_id: str, audio: bool):
        product = await self.get_by_product_id(product_id)
        if product:
            product.audio_ru = audio
