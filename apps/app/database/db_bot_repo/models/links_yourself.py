from sqlalchemy import Column, Integer, String

from apps.app.database.db_bot_repo.models.base import Base, BaseMixin


class LinkYourself(Base, BaseMixin):
    __tablename__ = "link_yourself"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
