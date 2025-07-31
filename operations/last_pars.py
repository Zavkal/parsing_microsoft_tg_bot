from database.db_bot_repo.repositories.parser_schedule import ParserScheduleRepository
from entities.parser_entity import ParserName


async def get_last_pars(repo_conf: ParserScheduleRepository) -> tuple[str, str, str]:
    config = await repo_conf.get_all_schedule_conditions()
    last_pars_price_products = config.get(ParserName.PARS_PRICE)[0].get('last_run')
    last_pars_products = config.get(ParserName.BIG_PARSER)[0].get('last_run')
    last_pars_sale = config.get(ParserName.SALE)[0].get('last_run')
    return last_pars_price_products, last_pars_products, last_pars_sale