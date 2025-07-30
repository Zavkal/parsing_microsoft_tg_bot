from contextlib import asynccontextmanager
import aiosqlite

from config import DEFAULT_SCHEDULES


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
            await conn.execute("""CREATE TABLE IF NOT EXISTS parser_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parser_name TEXT NOT NULL,              -- Название парсера: 'sale', 'products', 'new_products'
                frequency TEXT NOT NULL,
                day_of_week INTEGER,              -- День недели: 'monday', 'tuesday', и т.п.
                day_of_month INTEGER,
                time TEXT NOT NULL,                     -- Время запуска в формате HH:MM
                is_enabled INTEGER DEFAULT 0,           -- Включено ли расписание
                last_run TEXT                           -- Последний запуск (опционально, для логов)
            );
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

                # Проверяем, есть ли записи
                cursor = await conn.execute("SELECT COUNT(*) FROM parser_schedule")
                count = (await cursor.fetchone())[0]
                if count == 0:
                    for row in DEFAULT_SCHEDULES:
                        await conn.execute("""
                                           INSERT INTO parser_schedule (parser_name, frequency, day_of_week,
                                                                        day_of_month, time)
                                           VALUES (?, ?, ?, ?, ?)
                                           """, (
                                               row["parser_name"],
                                               row["frequency"],
                                               row["day_of_week"],
                                               row["day_of_month"],
                                               row["time"]
                                           ))
                    await conn.commit()

                await conn.close()




