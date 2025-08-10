from sqlalchemy import select

from database.db_bot import DataBase
from database.db_bot_repo.models.links_yourself import LinkYourself


class LinkYourselfRepository:

    def __init__(self, db: DataBase):
        self.db = db

    async def get_all_links_yourself(self, ) -> list:
        async with self.db.get_session() as session:
            stmt = select(LinkYourself.url)
            result = session.execute(stmt).scalars().all()
            return [link for link in result]


    async def create_new_link_yourself(self, url: LinkYourself) -> None:
        async with self.db.get_session() as session:
            session.add(url)


    async def delete_links_yourself(self, url: LinkYourself) -> None:
        async with self.db.get_session() as session:
            session.delete(url.url)