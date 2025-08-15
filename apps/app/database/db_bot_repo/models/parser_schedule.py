from sqlalchemy import Column, Integer, String, Boolean

from apps.app.database.db_bot_repo.models.base import Base, BaseMixin


class ParserSchedule(Base, BaseMixin):
    __tablename__ = "parser_schedule"

    id = Column(Integer, primary_key=True)
    parser_name = Column(String)
    frequency = Column(String, nullable=True)
    day_of_week = Column(String, nullable=True)
    day_of_month = Column(String, nullable=True)
    time_pars = Column(String, nullable=True)
    is_enabled = Column(Boolean, nullable=False)
    last_run = Column(String, nullable=True)
