from sqlalchemy import Column, Integer, Boolean

from apps.core.database.db_bot_repo.models.base import Base, BaseMixin


class Country(Base, BaseMixin):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    IN = Column(Boolean)
    NG = Column(Boolean)
    US = Column(Boolean)
    AR = Column(Boolean)
    TR = Column(Boolean)
    UA = Column(Boolean)
