from config import FREQUENCY_RU, DAYS_OF_WEEK_RU
from apps.core.database.repositories_manager import RepoManager
from apps.parser.entities.parser_entity import ParserName


async def generate_text_auto_pars(repo_manager: RepoManager):
    config = await repo_manager.parser_schedule_repo.get_all_schedule_conditions()
    new_price = config.get(ParserName.PARS_PRICE)[0]
    big_pars = config.get(ParserName.BIG_PARSER)[0]
    sale_pars = config.get(ParserName.SALE)[0]

    text = (
    f"⚙️ <b>Настройки автопарсинга</b>:\n\n"
    f"🛒 <b>Цены:</b>\n"
    f"  {format_schedule(new_price)}\n\n"
    f"📦 <b>Распродажи:</b>\n"
    f"  {format_schedule(sale_pars)}\n\n"
    f"📊 <b>Общая база:</b>\n"
    f"  {format_schedule(big_pars)}"
)
    return text

def format_schedule(parser_data: dict) -> str:
    if not parser_data or not parser_data.get("is_enabled"):
        return "❌ Выключено"

    freq = parser_data.get("frequency")
    time = parser_data.get("time_pars", "00:00")
    day_of_week = parser_data.get("day_of_week")
    day_of_month = parser_data.get("day_of_month")

    if freq == "daily":
        return f"{FREQUENCY_RU[freq]} в {time}"
    elif freq == "weekly":
        weekday = DAYS_OF_WEEK_RU.get(day_of_week)
        return f"{FREQUENCY_RU[freq]} в {weekday} в {time}"
    elif freq == "monthly":
        return f"{FREQUENCY_RU[freq]} {day_of_month}-го числа в {time}"
    else:
        return "❓ Неизвестная конфигурация"
