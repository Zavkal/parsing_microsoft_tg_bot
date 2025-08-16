from config import regions, regions_name
from config_bot import repo_manager


async def generate_text_pars_sale_settings() -> str:
    country = await repo_manager.country_repo.get_all_county_pars_sale()
    text = "Регионы для копирования цен:\n"
    for region in regions:
        if country.get(region):
            text += regions_name.get(region) + "\n"
    all_links =  await repo_manager.link_yourself_repo.get_all_links_yourself()
    text += "\n\nСсылки:\n" + "\n".join(all_links)
    return text