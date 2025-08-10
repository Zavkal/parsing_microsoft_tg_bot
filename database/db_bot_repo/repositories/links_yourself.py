from database.db_bot import DataBase


class LinksYourselfRepository:

    def __init__(self, db: DataBase):
        self.db = db

    async def get_all_links_yourself(self, ) -> list:
        async with self.db.get_session() as conn:
            cursor = await conn.execute('SELECT * FROM links_yourself')
            rows = await cursor.fetchall()
            return [row[0] for row in rows]


    async def create_new_link_yourself(self, url: str) -> None:
        async with self.db.get_session() as conn:
            await conn.execute(
                "INSERT INTO links_yourself SET url = ?",
                (url,)
            )
            await conn.commit()


    async def delete_links_yourself(self, url: str) -> None:
        async with self.db.get_session() as conn:
            cursor = await conn.execute(
                'DELETE FROM links_yourself WHERE url = ?',
                (url,)
            )
            await conn.commit()