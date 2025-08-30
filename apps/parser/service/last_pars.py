from apps.core.database.repositories_manager import RepoManager
from apps.parser.entities.parser_entity import ParserName


async def get_last_pars(repo_manager: RepoManager) -> tuple[str, str, str]:
    config = await repo_manager.parser_schedule_repo.get_all_schedule_conditions()
    last_pars_price_products = config.get(ParserName.PARS_PRICE)[0].get('last_run')
    last_pars_products = config.get(ParserName.BIG_PARSER)[0].get('last_run')
    last_pars_sale = config.get(ParserName.SALE)[0].get('last_run')
    return last_pars_price_products, last_pars_products, last_pars_sale