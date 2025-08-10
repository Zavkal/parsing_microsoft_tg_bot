from sqlalchemy import select, update

from database.db import DataBase
from database.db_repo.models.formulas import Formulas


class FormulasRepository:

    def __init__(self, db: DataBase):
        self.db = db


    async def get_formulas(self, ) -> dict:
        async with self.db.get_session() as session:
            smtm = select(Formulas)
            result = await session.execute(smtm)
            columns = result.keys()
            row = result.fetchone()

            return dict(zip(columns, row))


    async def update_formulas(
            self,
            country_name: str,
            formula: str,
    ) -> None:
        async with self.db.get_session() as session:
            smtm = update(Formulas).values({country_name: formula})
            await session.execute(smtm)

