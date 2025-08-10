from sqlalchemy import Column, Integer, String, Boolean

from database.db_bot_repo.models.base import Base


class ParserSchedule(Base):
    __tablename__ = "parser_schedule"

    id = Column(Integer, primary_key=True)
    parser_name = Column(String)
    frequency = Column(String)
    day_of_week = Column(String)
    day_of_month = Column(String)
    time_pars = Column(String)
    is_enabled = Column(Boolean)
    last_run = Column(String)
