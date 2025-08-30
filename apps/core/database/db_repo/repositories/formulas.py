from sqlalchemy import select, update

from apps.core.database.db import DataBase
from apps.core.database.db_repo.models.formulas import Formulas


class FormulasRepository:

    def __init__(self, db: DataBase):
        self.db = db

    async def get_formulas(self) -> dict:
        async with self.db.get_session() as session:
            result = await session.execute(select(Formulas))
            formula = result.scalars().first()  # получаем объект модели
            if formula:
                return {
                    "IN": formula.IN,
                    "NG": formula.NG,
                    "US": formula.US,
                    "AR": formula.AR,
                    "TR": formula.TR,
                    "UA": formula.UA,
                }
            return {}


    async def update_formulas(
            self,
            country_name: str,
            formula: str,
    ) -> None:
        async with self.db.get_session() as session:
            smtm = update(Formulas).values({country_name: formula})
            await session.execute(smtm)

