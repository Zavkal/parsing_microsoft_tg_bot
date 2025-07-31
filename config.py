import logging
import pytz

from entities.parser_entity import ParserName

# Указываем часовой пояс Москвы
moscow_tz = pytz.timezone("Europe/Moscow")

ADMIN = "1637636761"  # 763197387 585028070 1637636761

regions = ["IN", "NG", "US", "AR", "TR", "UA"]

regions_id = {"IN": "en-IN",
              "NG": "en-NG",
              "US": "en-US",
              "AR": "es-AR",
              "TR": "tr-TR",
              "UA": "uk-UA"}

regions_name = {
        "IN": "🇪🇬 Египет",
        "NG": "🇳🇬 Нигерия",
        "US": "🇺🇸 Сша",
        "AR": "🇦🇷 Аргентина",
        "TR": "🇹🇷 Турция",
        "UA": "🇺🇦 Украина",
    }


main_game_list = [
    'https://www.xbox.com/eu-EN/games/browse?orderby=Title+Desc',
    'https://www.xbox.com/eu-EN/games/browse?orderby=Title+Asc'
]


product_pass = {
    'CFQ7TTC0QH5H': "UBISOFT+",
    'CFQ7TTC0K6L8': 'Xbox Game Pass Ultimate',
    'CFQ7TTC0KGQ8': 'PC Game Pass',
    'CFQ7TTC0P85B': 'Xbox Game Pass Standard',
    'CFQ7TTC0K5DJ': 'Xbox Game Pass Core',

}

DEFAULT_SCHEDULES = [
    {
        "parser_name": ParserName.SALE,
        "frequency": "weekly",
        "day_of_week": "monday",
        "day_of_month": None,
        "time": "10:30"
    },
    {
        "parser_name": ParserName.BIG_PARSER,
        "frequency": "weekly",
        "day_of_week": "friday",
        "day_of_month": None,
        "time": "11:00"
    },
    {
        "parser_name": ParserName.PARS_PRICE,
        "frequency": "monthly",
        "day_of_week": None,
        "day_of_month": 1,
        "time": "14:00"
    }
]

parsing_name = {
    "sale_products": "Распродажи",
    "products": "Биг парсер",
    "price_products": "Цены"}


DAYS_OF_WEEK_RU = {
    "monday": "Понедельник",
    "tuesday": "Вторник",
    "wednesday": "Среда",
    "thursday": "Четверг",
    "friday": "Пятница",
    "saturday": "Суббота",
    "sunday": "Воскресенье"
}

FREQUENCY_RU = {
    "daily": "Ежедневно",
    "weekly": "Еженедельно",
    "monthly": "Ежемесячно"
}




link = 'https://www.xbox.com/en-US/games/browse/game-deals'
logging.basicConfig(level=logging.INFO)