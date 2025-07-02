from database.db_bot_repo.repositories.config import ConfigRepository


async def get_last_pars(repo_conf: ConfigRepository) -> tuple:
    config = await repo_conf.get_config()
    last_pars_new_products = config.get("last_pars_new_products")
    last_date_pars_products = config.get("last_date_pars_products")
    last_date_pars_sale = config.get("last_date_pars_sale")
    return last_pars_new_products, last_date_pars_products, last_date_pars_sale