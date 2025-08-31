from config_bot import repo_manager
from apps.parser.service.calculate import calculate_price


async def save_data_in_list(sort_by=True):
    all_sale_products = await repo_manager.product_repo.get_all_sale_product_id()
    game_entries = []  # Временный список для сортировки

    for product_id in all_sale_products:
        game = await repo_manager.product_repo.get_product_by_product_id(product_id=product_id)
        all_price = await repo_manager.product_price_repo.get_prices_by_product(product_id=product_id)
        us_price = None
        ng_ua_prices = []
        ar_tr_prices = []
        discount_percentage = None

        # Проходим по всем странам и данным
        for country_code, price_data in all_price.items():
            if not price_data:  # Если данных по стране нет — пропускаем
                continue

            orig_price, disc_price = await calculate_price(
                original_price=price_data.get("original_price"),
                discounted_price=price_data.get('discounted_price'),
                country_code=country_code,
            )
            if orig_price == disc_price:  # Если нет скидки — пропускаем
                continue

            if country_code == 'US':
                us_price = disc_price

            if country_code in ['NG', 'UA']:
                ng_ua_prices.append(disc_price)

            if country_code in ['AR', 'TR']:
                ar_tr_prices.append(disc_price)

            # Берем первую доступную скидку (если её ещё нет)
            if discount_percentage is None:
                discount_percentage = price_data.get('discounted_percentage')

        # Если **нет цен вообще**, пропускаем игру
        if us_price is None and not ng_ua_prices and not ar_tr_prices:
            continue

        # Формируем строку с ценами
        price_lines = []
        if discount_percentage is not None:
            price_lines.append(f"{game.get('game_name')} (-{int(discount_percentage)}%)")

        if us_price is not None:
            price_lines.append(f"Ключ - {int(round(us_price, -1))}р")

        if ng_ua_prices:
            min_ng_ua_price = min(ng_ua_prices)
            price_lines.append(f"Ваш аккаунт - {int(round(min_ng_ua_price, -1))}р")

        if ar_tr_prices:
            min_ar_tr_price = min(ar_tr_prices)
            price_lines.append(f"Новый аккаунт - {int(round(min_ar_tr_price, -1))}р")

        price_lines.append("•————————————————")  # Разделитель
        game_entries.append({
            "name": game.get('game_name'),
            "is_dlc": game.get('is_dlc', False),
            "line": "\n".join(price_lines) + "\n"  # Объединяем строки
        })

    # **Сортировка по названию, DLC в конец**
    if sort_by:
        game_entries.sort(
            key=lambda x: (x["is_dlc"], x["name"].lower())  # DLC (True) в конец, названия по алфавиту
        )

    # **Добавляем буквы-разделители**
    sorted_lines = []
    current_letter = None

    for entry in game_entries:
        first_letter = entry["name"][0].upper()  # Первая буква названия игры

        if first_letter != current_letter:  # Если буква изменилась
            sorted_lines.append(f"\n{first_letter}\n\n")  # Добавляем заголовок
            current_letter = first_letter  # Обновляем текущую букву

        sorted_lines.append(entry["line"])  # Добавляем саму игру

    # Записываем в файл
    with open("games_prices.txt", "w", encoding="utf-8") as file:
        file.writelines(sorted_lines)


