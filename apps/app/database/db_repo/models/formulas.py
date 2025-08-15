from sqlalchemy import Column, Integer, String

from apps.app.database.db_repo.models.base import Base, BaseMixin


class Formulas(Base, BaseMixin):
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True)
    IN = Column(String)
    NG = Column(String)
    US = Column(String)
    AR = Column(String)
    TR = Column(String)
    UA = Column(String)
