from database.db_bot import DataBase


class ParserScheduleRepository:
    def __init__(self, db: DataBase):
        self.db = db


    async def update_last_run(self, parser_name: str, date: str) -> None:
        async with self.db.get_session() as conn:
            await conn.execute(
                "UPDATE parser_schedule SET last_run = ? WHERE parser_name = ?",
                (date, parser_name)
            )
            await conn.commit()


    async def update_status_pars(self, parser_name: str, is_enabled: bool) -> None:
        async with self.db.get_session() as conn:
            await conn.execute(
                "UPDATE parser_schedule SET is_enabled = ? WHERE parser_name = ?",
                (is_enabled, parser_name)
            )
            await conn.commit()


    async def get_enabled_schedules(self) -> list[dict]:
        async with self.db.get_session() as conn:
            cursor = await conn.execute(
                "SELECT * FROM parser_schedule WHERE is_enabled = 1"
            )
            rows = await cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]


    async def get_schedule_by_parser(self, parser_name: str) -> dict | None:
        async with self.db.get_session() as conn:
            cursor = await conn.execute(
                "SELECT * FROM parser_schedule WHERE parser_name = ?",
                (parser_name,)
            )
            row = await cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            return None


    async def get_all_schedule_conditions(self) -> dict[str, list[dict]]:
        async with self.db.get_session() as conn:
            cursor = await conn.execute("""
                SELECT * FROM parser_schedule
                                        """)
            rows = await cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            result = {}

            for row in rows:
                row_dict = dict(zip(columns, row))
                parser = row_dict["parser_name"]
                result.setdefault(parser, []).append(row_dict)

            return result


    async def update_parser_schedule(self, parser_name: str, **fields) -> None:
        if not fields:
            return

        async with self.db.get_session() as conn:
            # Формируем часть SQL с полями: "field1 = ?, field2 = ?, ..."
            set_clause = ", ".join(f"{key} = ?" for key in fields.keys())
            values = list(fields.values())
            values.append(parser_name)  # для WHERE

            query = f"UPDATE parser_schedule SET {set_clause} WHERE parser_name = ?"
            await conn.execute(query, values)
            await conn.commit()