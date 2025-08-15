# import asyncio
# import logging
# from datetime import datetime
#
# class AutoParserScheduler:
#     def __init__(self, get_session, check_interval=60):
#         self.get_session = get_session
#         self.check_interval = check_interval  # в секундах
#
#     async def run(self):
#         while True:
#             try:
#                 await self.check_and_run_tasks()
#             except Exception as e:
#                 logging.error(f"[AutoParserScheduler] Error: {e}")
#             await asyncio.sleep(self.check_interval)
#
#     async def check_and_run_tasks(self):
#         now = datetime.now()
#         current_time = now.strftime("%H:%M")
#         current_day_of_week = now.weekday()
#         current_day_of_month = now.day
#
#         async with self.get_session() as conn:
#             result = await conn.execute("""
#                 SELECT id, parser_name, frequency, day_of_week, day_of_month, time, last_run
#                 FROM parser_schedule
#                 WHERE is_enabled = 1
#             """)
#             rows = await result.fetchall()
#
#         for row in rows:
#             should_run = self._should_run(row, now, current_time)
#             if should_run:
#                 await self._run_parser_and_update_last_run(row, now)
#
#     def _should_run(self, row, now, current_time):
#         if row['time'] != current_time:
#             return False
#
#         if row['last_run'] == now.strftime("%Y-%m-%d %H:%M"):
#             return False  # уже запущено в эту минуту
#
#         match row['frequency']:
#             case 'daily':
#                 return True
#             case 'weekly':
#                 return row['day_of_week'] == now.weekday()
#             case 'monthly':
#                 return row['day_of_month'] == now.day
#         return False
#
#     async def _run_parser_and_update_last_run(self, row, now):
#         logging.error(f"Запускаю парсер: {row['parser_name']}")
#
#         await run_parser(row['parser_name'])  # ты реализуешь run_parser(parser_name)
#
#         async with self.get_session() as conn:
#             await conn.execute("""
#                 UPDATE parser_schedule SET last_run = ?
#                 WHERE id = ?
#             """, (now.strftime("%Y-%m-%d %H:%M"), row['id']))
