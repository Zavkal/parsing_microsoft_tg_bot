from database.db_bot import DataBase


class ConfigRepository:
    def __init__(self, db: DataBase):
        self.db = db


    async def update_date_pars(self, pars_tag: str, date: str) -> None:
        async with self.db.get_session() as conn:
            # Используем параметризованный запрос для безопасности
            query = f'UPDATE config SET "{pars_tag}" = ? WHERE id = 1'
            await conn.execute(query, (date,))


    async def get_config(self, ) -> dict:
        async with self.db.get_session() as conn:
            cursor = await conn.execute("SELECT * FROM config WHERE id = 1")
            row = await cursor.fetchone()  # Получаем одну строку

            columns = [desc[0] for desc in cursor.description]

            # Преобразуем кортеж row в словарь, используя названия колонок
            result = dict(zip(columns, row))
            return result