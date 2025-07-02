from database.db_bot import DataBase


class CountryRepository:
    def __init__(self, db: DataBase):
        self.db = db

    async def get_all_county_pars(self, ):
        async with self.db.get_session() as conn:
            cursor = conn.execute('SELECT * FROM country')
            row = cursor.fetchall()[0]
            return {
                "IN": row[1],
                "NG": row[2],
                "US": row[3],
                "AR": row[4],
                "TR": row[5],
                "UA": row[6],
            }

    async def update_region_pars(self, region: str, status: int):
        async with self.db.get_session() as conn:
            query = f'UPDATE country SET "{region}" = ?'
            conn.execute(query, (status,))
            conn.commit()