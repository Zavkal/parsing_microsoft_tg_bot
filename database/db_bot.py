from contextlib import asynccontextmanager
import aiosqlite


class DataBase:
    def __init__(self, db_path: str = "db_bot.db"):
        self.db_path = db_path


    @asynccontextmanager
    async def get_session(self):
        conn = await aiosqlite.connect(self.db_path)
        try:
            yield conn
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise
        finally:
            await conn.close()


    async def start_db(self, ):
        async with self.get_session() as conn:
            await conn.execute("""CREATE TABLE IF NOT EXISTS config(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_date_pars_sale TEXT,
                time_pars_sale TEXT,
                last_date_pars_products TEXT,
                time_pars_products TEXT,
                last_pars_new_products TEXT,
                time_pars_new_products TEXT
                )
                """)

            await conn.execute("""CREATE TABLE IF NOT EXISTS country(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "IN" BOOL DEFAULT 0,
                NG BOOl DEFAULT 0,
                US BOOl DEFAULT 0,
                AR BOOl DEFAULT 0,
                TR BOOl DEFAULT 0,
                UA BOOl DEFAULT 0
                )
                """)

            await conn.execute("""CREATE TABLE IF NOT EXISTS country_price(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "IN" BOOL DEFAULT 0,
                NG BOOl DEFAULT 0,
                US BOOl DEFAULT 0,
                AR BOOl DEFAULT 0,
                TR BOOl DEFAULT 0,
                UA BOOl DEFAULT 0
                )
                """)

            # Проверяем, есть ли записи в таблице country
            cursor = await conn.execute("SELECT COUNT(*) FROM country")
            count = await cursor.fetchone()

            # Если записей нет, добавляем начальную строку
            if count == 0:
                await conn.execute("""
                        INSERT INTO country ("IN", NG, US, AR, TR, UA)
                        VALUES (0, 0, 0, 0, 0, 0)
                    """)

            # Проверяем, есть ли записи в таблице country
            cursor = await conn.execute("SELECT COUNT(*) FROM country_price")
            count = await cursor.fetchone()

            # Если записей нет, добавляем начальную строку
            if count == 0:
                await conn.execute("""
                        INSERT INTO country_price ("IN", NG, US, AR, TR, UA)
                        VALUES (0, 0, 0, 0, 0, 0)
                    """)





