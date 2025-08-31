import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio

from apps.parser.entities.parser_entity import ParserName
from apps.parser.service.start_big_parser import start_big_parser_products
from apps.parser.service.start_price_pars import start_price_pars_products
from apps.parser.service.start_sale_pars import start_sale_pars
from config import ADMIN
from config_bot import repo_manager, bot


class ParserSchedulerManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.scheduler = AsyncIOScheduler()
            cls._instance.scheduler.start()
            cls._instance.jobs = {}
        return cls._instance

    async def refresh_schedule(self, ):
        parsers = await repo_manager.parser_schedule_repo.get_enabled_schedules()

        # удаляем старые задачи
        for job_id in list(self.jobs.keys()):
            self.scheduler.remove_job(job_id)
            del self.jobs[job_id]

        # создаём новые задачи
        for parser in parsers:
            hour, minute = map(int, parser.get("time_pars").split(":"))
            if parser.get("frequency") == "daily":
                trigger = CronTrigger(hour=hour, minute=minute)

            elif parser.get("frequency") == "weekly" and parser.get("day_of_week"):
                trigger = CronTrigger(day_of_week=parser.get("day_of_week").lower(), hour=hour, minute=minute)

            elif parser.get("frequency") == "monthly" and parser.get("day_of_month"):
                trigger = CronTrigger(day=int(parser.get("day_of_month")), hour=hour, minute=minute)

            else:
                logging.error(f"ОШИБКА СОЗДАНИЯ АВТОПАРСА {parser.get('parser_name')}")
                continue

            print(trigger)

            job = self.scheduler.add_job(
                self.run_parser, trigger, args=[parser.get("parser_name")], id=str(parser.get("id")),
            )
            self.jobs[str(parser.get("id"))] = job

    @staticmethod
    async def run_parser(parser_name: str) -> None:
        logging.info(f"Запуск парсера: {parser_name}")
        bot.send_message(
            chat_id=ADMIN,
            text=f"Был запущен автопарс {parser_name}",
        )

        if parser_name == ParserName.SALE:
            await start_sale_pars()
        elif parser_name == ParserName.BIG_PARSER:
            await start_big_parser_products()
        elif parser_name == ParserName.PARS_PRICE:
            await start_price_pars_products()
        bot.send_message(
            chat_id=ADMIN,
            text=f"Был окончен автопарс {parser_name}",
        )

        logging.info(f"Парсер {parser_name} завершил работу")
