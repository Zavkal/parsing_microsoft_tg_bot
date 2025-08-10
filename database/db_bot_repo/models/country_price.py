from sqlalchemy import Column, Integer, Boolean

from database.db_bot_repo.models.base import Base


class CountryPrice(Base):
    __tablename__ = "country_price"

    id = Column(Integer, primary_key=True)
    IN = Column(Boolean)
    NG = Column(Boolean)
    US = Column(Boolean)
    AR = Column(Boolean)
    TR = Column(Boolean)
    UA = Column(Boolean)
