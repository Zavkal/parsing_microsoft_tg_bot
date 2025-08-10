import asyncio

from database.db import get_exchange, get_formulas, save_ru_price_by_country


def calculate_price(
        country_code: str,
        original_price: float,
        discounted_price: float
) -> tuple[float, float]:
    formula = get_formulas().get(country_code)
    exchange_rate = get_exchange()
    if original_price < 1 and discounted_price < 1:
        return 0, 0

    if "IN" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "NG" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "US" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)
        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "AR" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "TR" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "UA" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    else:
        return f"error: Нет такой страны - {country_code}"

# async def calculate_price_all_country(country_code, price):
#
#     _, ru_price = calculate_price(country_code, price, price)
#
#     save_ru_price_by_country(product_id=product_id,
#                              country_code=country_code,
#                              ru_price=ru_price)
