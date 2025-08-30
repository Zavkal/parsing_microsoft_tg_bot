from apps.core.database.db import DataBase as DataBase_db
from apps.core.database.db_bot import DataBase as DataBase_db_bot
from apps.core.database.db_bot_repo.repositories.country import CountryRepository
from apps.core.database.db_bot_repo.repositories.country_price import CountryPriceRepository
from apps.core.database.db_bot_repo.repositories.links_yourself import LinkYourselfRepository
from apps.core.database.db_bot_repo.repositories.parser_schedule import ParserScheduleRepository
from apps.core.database.db_repo.repositories.exchange import ExchangeRepository
from apps.core.database.db_repo.repositories.formulas import FormulasRepository

from apps.core.database.db_repo.repositories.product_price import ProductPriceRepository
from apps.core.database.db_repo.repositories.product import ProductRepository


class RepoManager:
    def __init__(self, db: DataBase_db, db_bot: DataBase_db_bot):
        # Работа с ботом
        self.parser_schedule_repo = ParserScheduleRepository(db_bot)
        self.country_price_repo = CountryPriceRepository(db_bot)
        self.country_repo = CountryRepository(db_bot)
        self.link_yourself_repo = LinkYourselfRepository(db_bot)

        # Работа с продуктами
        self.product_repo = ProductRepository(db)
        self.product_price_repo = ProductPriceRepository(db)

        # Работа с ценами
        self.exchange_repo = ExchangeRepository(db)
        self.formulas_repo = FormulasRepository(db)