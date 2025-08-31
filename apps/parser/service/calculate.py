import logging

from config_bot import repo_manager


async def calculate_price(
        country_code: str,
        original_price: float,
        discounted_price: float
) -> tuple[float, float]:
    try:
        formula = (await repo_manager.formulas_repo.get_formulas()).get(country_code)
        exchange_rate = await repo_manager.exchange_repo.get_exchange()
        if original_price < 1 and discounted_price < 1:
            return 0, 0

        original_price, discounted_price = _get_price_exchange(
            original_price=original_price,
            discounted_price=discounted_price,
            exchange_rate=exchange_rate,
            country_code=country_code,
        )

        if "IN" == country_code:
            if discounted_price > 2999:
                original_price += 200
                discounted_price += 200
            orig_price_formula, discounted_price_formula = _get_price_formulas(
                original_price=original_price,
                discounted_price=discounted_price,
                formula=formula,
            )
            return orig_price_formula, discounted_price_formula

        elif "NG" == country_code:
            if discounted_price > 2999:
                original_price += 200
                discounted_price += 200

            orig_price_formula, discounted_price_formula = _get_price_formulas(
                original_price=original_price,
                discounted_price=discounted_price,
                formula=formula,
            )
            return orig_price_formula, discounted_price_formula

        elif "US" == country_code:
            orig_price_formula, discounted_price_formula = _get_price_formulas(
                original_price=original_price,
                discounted_price=discounted_price,
                formula=formula,
            )
            return orig_price_formula, discounted_price_formula

        elif "AR" == country_code:
            if discounted_price > 2999:
                original_price += 200
                discounted_price += 200

            orig_price_formula, discounted_price_formula = _get_price_formulas(
                original_price=original_price,
                discounted_price=discounted_price,
                formula=formula,
            )
            return orig_price_formula, discounted_price_formula

        elif "TR" == country_code:
            if discounted_price > 2999:
                original_price += 200
                discounted_price += 200

            orig_price_formula, discounted_price_formula = _get_price_formulas(
                original_price=original_price,
                discounted_price=discounted_price,
                formula=formula,
            )
            return orig_price_formula, discounted_price_formula

        elif "UA" == country_code:
            if discounted_price > 2999:
                original_price += 200
                discounted_price += 200

            orig_price_formula, discounted_price_formula = _get_price_formulas(
                original_price=original_price,
                discounted_price=discounted_price,
                formula=formula,
            )
            return orig_price_formula, discounted_price_formula

        else:
            logging.error(f"Неизвестная страна: {country_code}")
            return 0, 0
    except Exception as e:
        logging.error(f"Ошибка при расчете цен {e}")


def _get_price_exchange(
        original_price: float,
        discounted_price: float,
        exchange_rate: dict,
        country_code: str):
    original_price = original_price * exchange_rate.get(country_code)
    discounted_price = discounted_price * exchange_rate.get(country_code)
    return original_price, discounted_price


def _get_price_formulas(
        original_price: float,
        discounted_price: float,
        formula: str) -> tuple[float, float]:
    original_price = round(eval(str(original_price) + formula), -1)
    discounted_price = round(eval(str(discounted_price) + formula), -1)
    return original_price, discounted_price


# async def calculate_price_all_country(country_code, price):
#
#     _, ru_price = calculate_price(country_code, price, price)
#
#     save_ru_price_by_country(product_id=product_id,
#                              country_code=country_code,
#                              ru_price=ru_price)
