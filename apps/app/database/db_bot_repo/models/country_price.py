from sqlalchemy import Column, Integer, Boolean

from apps.app.database.db_bot_repo.models.base import Base, BaseMixin


class CountryPrice(Base, BaseMixin):
    __tablename__ = "country_price"

    id = Column(Integer, primary_key=True)
    IN = Column(Boolean)
    NG = Column(Boolean)
    US = Column(Boolean)
    AR = Column(Boolean)
    TR = Column(Boolean)
    UA = Column(Boolean)
