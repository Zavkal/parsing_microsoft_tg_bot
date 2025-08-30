from sqlalchemy import select, update

from apps.core.database.db_bot import DataBase
from apps.core.database.db_bot_repo.models.country import Country


class CountryRepository:
    def __init__(self, db: DataBase):
        self.db = db

    async def get_all_county_pars_sale(self):
        async with self.db.get_session() as session:
            stmt = select(Country)
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

    async def update_region_pars(self, region: str, status: int):
        async with self.db.get_session() as session:
            stmt = update(Country).values({region: status})
            await session.execute(stmt)