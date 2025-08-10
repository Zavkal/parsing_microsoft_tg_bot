from sqlalchemy import Column, Integer, Float, String

from database.db_repo.models.base import Base


class Exchange(Base):
    __tablename__ = "exchange"

    id = Column(Integer, primary_key=True)
    date_exchanged = Column(String)
    IN = Column(Float)
    NG = Column(Float)
    US = Column(Float)
    AR = Column(Float)
    TR = Column(Float)
    UA = Column(Float)
