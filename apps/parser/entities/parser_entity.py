from enum import StrEnum


class ParserName(StrEnum):
    SALE = 'sale_products' # => Распродажи
    BIG_PARSER = 'products' # => Большой парсер
    PARS_PRICE = 'price_products' # => Парсинг новых продуктов
