from sqlalchemy import select, delete

from apps.core.database.db_bot import DataBase
from apps.core.database.db_bot_repo.models.links_yourself import LinkYourself


class LinkYourselfRepository:

    def __init__(self, db: DataBase):
        self.db = db

    async def get_all_links_yourself(self, ) -> list:
        async with self.db.get_session() as session:
            stmt = select(LinkYourself.url)
            result = await session.execute(stmt)
            return [link for link in result.scalars().all()]


    async def create_new_link_yourself(self, url: str) -> None:
        async with self.db.get_session() as session:
            link = LinkYourself(url=url)
            session.add(link)


    async def delete_link_yourself(self, url: str) -> None:
        async with self.db.get_session() as session:
            await session.execute(
                delete(LinkYourself).where(LinkYourself.url == url)
            )