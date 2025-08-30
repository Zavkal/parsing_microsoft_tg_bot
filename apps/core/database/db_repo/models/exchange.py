from sqlalchemy import Column, Integer, Float, String

from apps.core.database.db_repo.models.base import Base, BaseMixin


class Exchange(Base, BaseMixin):
    __tablename__ = "exchange"

    id = Column(Integer, primary_key=True)
    date_exchanged = Column(String)
    IN = Column(Float)
    NG = Column(Float)
    US = Column(Float)
    AR = Column(Float)
    TR = Column(Float)
    UA = Column(Float)
