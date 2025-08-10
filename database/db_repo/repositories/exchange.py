from sqlalchemy import select, update

from database.db import DataBase
from database.db_repo.models.exchange import Exchange


class ExchangeRepository:

    def __init__(self, db: DataBase):
        self.db = db

    async def get_exchange(self) -> dict:
        async with self.db.get_session() as session:
            result = await session.execute(select(Exchange))
            columns = result.keys()
            row = result.fetchone()

            return dict(zip(columns, row))

    async def update_exchange(
            self,
            date_exchange: str,
            usd_to_rub: float,
            try_to_rub: float,
            ngn_to_rub: float,
            ars_to_rub: float,
            uah_to_rub: float,
            egp_to_rub: float,
    ) -> None:
        async with self.db.get_session() as session:
            stmt = update(Exchange).values(
                date_exchange=date_exchange,
                US=usd_to_rub,
                TR=try_to_rub,
                NG=ngn_to_rub,
                AR=ars_to_rub,
                UA=uah_to_rub,
                IN=egp_to_rub
            )
            await session.execute(stmt)

