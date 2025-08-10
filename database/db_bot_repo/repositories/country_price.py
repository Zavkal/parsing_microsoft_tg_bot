from sqlalchemy import select, update

from database.db_bot import DataBase
from database.db_bot_repo.models.country_price import CountryPrice


class CountyPriceRepository:

    def __init__(self, db: DataBase):
        self.db = db


    async def get_all_county_pars_product(self, ) -> dict:
        async with self.db.get_session() as session:
            stmt = select(CountryPrice)
            result = await session.execute(stmt)
            row = result.scalar_one()
            return {
                "IN": row.IN,
                "NG": row.NG,
                "US": row.US,
                "AR": row.AR,
                "TR": row.TR,
                "UA": row.UA,
        }


    async def update_region_pars_product(self, region: str, status: int):
        async with self.db.get_session() as session:
            stmt = update(CountryPrice).values({region: status})
            await session.execute(stmt)
