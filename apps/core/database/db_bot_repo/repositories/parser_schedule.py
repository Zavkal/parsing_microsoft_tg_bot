from sqlalchemy import update, select

from apps.core.database.db_bot import DataBase
from apps.core.database.db_bot_repo.models.parser_schedule import ParserSchedule


class ParserScheduleRepository:
    def __init__(self, db: DataBase):
        self.db = db


    async def update_last_run(self, parser_name: str, date: str) -> None:
        async with self.db.get_session() as session:
            await session.execute(
                update(ParserSchedule)
                .where(ParserSchedule.parser_name == parser_name)
                .values(last_run=date)
            )

    async def update_status_pars(self, parser_name: str, is_enabled: bool) -> None:
        async with self.db.get_session() as session:
            await session.execute(
                update(ParserSchedule)
                .where(ParserSchedule.parser_name == parser_name)
                .values(is_enabled=is_enabled)
            )

    async def get_enabled_schedules(self) -> list[dict]:
        async with self.db.get_session() as session:
            result = await session.execute(
                select(ParserSchedule).where(ParserSchedule.is_enabled)
            )
            return [s.to_dict() for s in result.scalars().all()]

    async def get_schedule_by_parser(self, parser_name: str) -> dict | None:
        async with self.db.get_session() as session:
            result = await session.execute(
                select(ParserSchedule).where(ParserSchedule.parser_name == parser_name)
            )
            return result.scalars().one().to_dict()

    async def get_all_schedule_conditions(self) -> dict[str, list[dict]]:
        async with self.db.get_session() as session:
            result = await session.execute(select(ParserSchedule))
            schedules = result.scalars().all()  # <- получаем объекты модели, а не Row

            grouped: dict[str, list[dict]] = {}
            for schedule in schedules:
                grouped.setdefault(schedule.parser_name, []).append(schedule.to_dict())
            return grouped

    async def update_parser_schedule(self, parser_name: str, **fields) -> None:
        if not fields:
            return
        async with self.db.get_session() as session:
            await session.execute(
                update(ParserSchedule)
                .where(ParserSchedule.parser_name == parser_name)
                .values(**fields)
            )