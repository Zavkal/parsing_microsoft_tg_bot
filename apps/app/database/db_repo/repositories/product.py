from sqlalchemy import select, update

from apps.app.database.db import DataBase
from apps.app.database.db_repo.models.product import Product
from apps.parser.entities.parser_data_entity import ProductDataEntity


class ProductRepository:

    def __init__(self, db: DataBase):
        self.db = db


    async def get_by_product_id(self, product_id: str):
        async with self.db.get_session() as session:
            stmt = select(Product).where(Product.product_id == product_id)
            result = await session.execute(stmt)
            return result.scalars().first()


    async def upsert_product(self, product_data: ProductDataEntity) -> None:
        async with self.db.get_session() as session:
            product = await self.get_by_product_id(product_data.product_id)
            if not product:
                product = Product(
                    product_id=product_data.product_id,
                    url_product=product_data.url_product,
                    game_name=product_data.game_name,
                    end_date_sale=product_data.end_date_sale,
                    device=product_data.device,
                    description=product_data.description,
                    short_description=product_data.short_description,
                    developer_name=product_data.developer_name,
                    publisher_name=product_data.publisher_name,
                    image_url=product_data.image_url,
                    pass_product_id=product_data.pass_product_id,
                    release_date=product_data.release_date,
                    capabilities=product_data.capabilities,
                    category=product_data.category,
                    link_video=product_data.link_video,
                    link_screenshot=product_data.link_screenshot,
                    game_weight=product_data.game_weight,
                    audio_ru=product_data.audio_ru,
                    interface_ru=product_data.interface_ru,
                    subtitles_ru=product_data.subtitles_ru,
                    sale_product=product_data.sale_product,
                    dlc=product_data.dlc,
                )
                session.add(product)
            else:
                product.url_product = product_data.url_product
                product.end_date_sale = product_data.end_date_sale
                product.device = product_data.device
                product.description = product_data.description
                product.short_description = product_data.short_description
                product.image_url = product_data.image_url
                product.pass_product_id = product_data.pass_product_id
                product.link_video = product_data.link_video
                product.link_screenshot = product_data.link_screenshot
                product.game_weight = product_data.game_weight
                product.audio_ru = product_data.audio_ru
                product.interface_ru = product_data.interface_ru
                product.subtitles_ru = product_data.subtitles_ru
                product.sale_product = product_data.sale_product
                product.dlc = product_data.dlc


    async def get_url_products(self) -> list[str]:
        async with self.db.get_session() as session:
            stmt = select(Product.url_product)
            result = await session.execute(stmt)
            return [row[0] for row in result.all()]


    async def set_sale_status_false_all_products(self, ) -> None:
        async with self.db.get_session() as session:
            stmt = update(Product).values(sale_product=False)
            await session.execute(stmt)


    async def set_sale_status_for_product(self, product_id: str) -> None:
        async with self.db.get_session() as session:
            stmt = update(Product).where(Product.product_id == product_id).values(sale_product=True)
            await session.execute(stmt)


    async def set_sale_status_true_for_products(self, product_ids: list[str]) -> None:
        async with self.db.get_session() as session:
            stmt = (
                update(Product)
                .where(Product.product_id.in_(product_ids))
                .values(sale_product=True)
            )
            await session.execute(stmt)


    async def remove_sale_status_for_product(self, product_id: str) -> None:
        async with self.db.get_session() as session:
            stmt = update(Product).where(Product.product_id == product_id).values(sale_product=False)
            await session.execute(stmt)


    async def update_end_date_sale_product(self, end_date_sale: str, product_id: str) -> None:
        async with self.db.get_session() as session:
            stmt = update(Product).where(Product.product_id == product_id).values(
                end_date_sale=end_date_sale
            )
            await session.execute(stmt)





