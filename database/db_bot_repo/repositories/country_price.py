from database.db_bot import DataBase


class CountyPriceRepository:

    def __init__(self, db: DataBase):
        self.db = db


    async def get_all_county_pars_product(self, ):
        async with self.db.get_session() as conn:
            cursor = await conn.execute('SELECT * FROM country_price')
            row = await cursor.fetchone()
            return {
                "IN": row[1],
                "NG": row[2],
                "US": row[3],
                "AR": row[4],
                "TR": row[5],
                "UA": row[6],
        }


    async def update_region_pars_product(self, region: str, status: int):
        async with self.db.get_session() as conn:
            # Используем параметризованный запрос для безопасности
            query = f'UPDATE country_price SET "{region}" = ? WHERE id = 1'
            await conn.execute(query, (status,))
            await conn.commit()