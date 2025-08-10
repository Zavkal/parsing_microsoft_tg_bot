from sqlalchemy import Column, Integer, String

from database.db_bot_repo.models.base import Base


class LinkYourself(Base):
    __tablename__ = "link_yourself"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
