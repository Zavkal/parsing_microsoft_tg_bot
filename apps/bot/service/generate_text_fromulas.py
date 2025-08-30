from apps.core.database.repositories_manager import RepoManager
from config import regions, regions_name


async def generate_text_formulas_settings(repo_manager: RepoManager) -> str:
    formulas: dict = await repo_manager.formulas_repo.get_formulas()
    text = "Ваши текущие формулы:\n\n"
    for region in regions:
        text += regions_name.get(region) + "\n" + f"Формула - прайс{formulas.get(region)}\n\n"

    return text