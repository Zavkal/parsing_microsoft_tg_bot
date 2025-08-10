import os
import sqlite3

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import regions_id
from entities.parser_data_entity import ProductDataEntity

base_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(base_dir, '../db.db')

conn = sqlite3.connect(db_path)
cur = conn.cursor()

class DataBase:
    def __init__(self, dsn: str):
        self.engine = create_async_engine(dsn, echo=False, future=True)
        self._session_factory = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    @asynccontextmanager
    async def get_session(self):
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


    def start_db():
        """
        ru-RU en-US es-AR tr-TR en-NG uk-UA en-IN \n -- Полное описание бд при создании
        *1. Уникальный id товара на сайте, \n
        *2. Ссылка на товар, \n
        *3. Название игры, \n
        *4. Окончание скидки, \n
        *5. Поддерживаемые платформы, \n
        *6. Описание, \n
        *7. Короткое описание, \n
        *8. Разработчик, \n
        *9. Публичное название разработчика, \n
        *10. Ссылка на постер товара, \n
        *11. Гейм пассы, \n
        *12. Дата выхода игры, \n
        *13. Возможности игры, \n
        *14. Категории, \n
        *15. Ссылка на трейлер, \n
        *16. Ссылка на скриншоты, \n
        *17. Вес игры
        *18. Русс озвучка, \n
        *19. Русс интерфейс, \n
        *20. Русс субтитры, \n
        *21. Является распродажей, \n
        *22. Основная игра этой dlc, \n
        """

        cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            url_product TEXT,
            game_name TEXT,
            end_date_sale TEXT,
            device TEXT,
            description TEXT,
            short_description TEXT,
            developer_name TEXT,
            publisher_name TEXT,
            image_url TEXT,
            pass_product_id TEXT,
            release_date TEXT,
            capabilities TEXT,
            category TEXT,
            link_video TEXT,
            link_screenshot TEXT,
            game_weight INTEGER,
            audio_ru INTEGER,
            interface_ru INTEGER,
            subtitles_ru INTEGER,
            sale_product INTEGER,
            dlc TEXT
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS "ru-RU" (
            product_id TEXT,
            original_price REAL,
            discounted_price REAL,
            discounted_percentage REAL,
            ru_price REAL,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS "en-US" (
            product_id TEXT,
            original_price REAL,
            discounted_price REAL,
            discounted_percentage REAL,
            ru_price REAL,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS "es-AR" (
            product_id TEXT,
            original_price REAL,
            discounted_price REAL,
            discounted_percentage REAL,
            ru_price REAL,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS "tr-TR" (
            product_id TEXT,
            original_price REAL,
            discounted_price REAL,
            discounted_percentage REAL,
            ru_price REAL,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS "en-NG" (
            product_id TEXT,
            original_price REAL,
            discounted_price REAL,
            discounted_percentage REAL,
            ru_price REAL,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS "uk-UA" (
            product_id TEXT,
            original_price REAL,
            discounted_price REAL,
            discounted_percentage REAL,
            ru_price REAL,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS "en-IN" (
            product_id TEXT,
            original_price REAL,
            discounted_price REAL,
            discounted_percentage REAL,
            ru_price REAL,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        ''')

        conn.commit()


    def add_product(data: ProductDataEntity):
        cur.execute("SELECT COUNT(*) FROM products WHERE product_id = ?", (data.product_id,))
        exists = cur.fetchone()[0] > 0

        if not exists:
            # Если записи нет, создаем новую
            cur.execute(
                '''INSERT INTO products (product_id, url_product, game_name, end_date_sale, device, description,
                                         short_description,
                                         developer_name, publisher_name, image_url, pass_product_id, release_date,
                                         capabilities, category, link_video, link_screenshot,
                                         game_weight, audio_ru, interface_ru, subtitles_ru, sale_product, dlc)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (data.product_id, data.url_product, data.game_name, data.end_date_sale, data.device, data.description, data.short_description,
                 data.developer_name, data.publisher_name, data.image_url, data.pass_product_id, data.release_date, data.capabilities, data.category,
                 data.link_video, data.link_screenshot, data.game_weight, data.audio_ru, data.interface_ru, data.subtitles_ru, data.sale_product, data.dlc)
            )

        else:
            pass

        conn.commit()


    def update_audio_product(audio: bool, product_id: str):
        cur.execute(
            'UPDATE products SET audio_ru = ? WHERE product_id = ?', (audio, product_id)
        )
        conn.commit()


    def update_interface_product(interface: bool, product_id: str):
        cur.execute(
            'UPDATE products SET interface_ru = ? WHERE product_id = ?', (interface, product_id)
        )
        conn.commit()


    def update_subtitles_product(subtitles: bool, product_id: str):
        cur.execute(
            'UPDATE poducts SET subtitles_ru = ? WHERE product_id = ?', (subtitles, product_id)
        )
        conn.commit()


    def update_capabilities_product(capabilities: str, product_id: str):
        cur.execute('UPDATE products SET capabilities = ? WHERE product_id = ?', (capabilities, product_id)
                    )
        conn.commit()


    def update_category_product(category: str, product_id: str):
        cur.execute('UPDATE products SET category = ? WHERE product_id = ?', (category, product_id)
                    )
        conn.commit()


    def update_description_product(description: str, product_id: str):
        cur.execute('UPDATE products SET description = ? WHERE product_id = ?', (description, product_id)
                    )
        conn.commit()


    def update_game_name_product(game_name: str, product_id: str):
        cur.execute('UPDATE products SET game_name = ? WHERE product_id = ?', (game_name, product_id)
                    )
        conn.commit()


    def update_end_date_sale_product(end_date_sale: str, product_id: str):
        cur.execute('UPDATE products SET end_date_sale = ? WHERE product_id = ?', (end_date_sale, product_id)
                    )
        conn.commit()


    def update_is_sale_product(product_id: str, count: int = 1):
        cur.execute('UPDATE products SET sale_product = ? WHERE product_id = ?', (count, product_id)
                    )
        conn.commit()


    def update_link_screenshots_product(link_screenshot: str, product_id: str):
        pass


    def update_price_products():
        pass


    def get_all_url_products():
        cur.execute('SELECT url_product FROM products')
        result = []
        for url in cur.fetchall():
            result.append(url[0])

        return result


    def get_all_sale_product():
        # Запрос для выборки данных
        cur.execute('SELECT product_id FROM products WHERE sale_product == 1;')

        result = []
        for url in cur.fetchall():
            result.append(url[0])

        return result


    def get_game_by_id(product_id: str):
        cur.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
        result = cur.fetchone()

        if result is None:
            return 0

        # Получение имен колонок
        columns = [desc[0] for desc in cur.description]

        # Создание словаря с данными
        game_data = dict(zip(columns, result))

        return game_data


    def get_url_products():
        cur.execute('SELECT url_product FROM products' )
        result = cur.fetchall()

        if result is None:
            return 0

        # Получение имен колонок
        url_list = [row[0] for row in result]
        return url_list


    def get_category_products():
        # Выполняем SQL-запрос
        cur.execute('SELECT category FROM products')
        result = cur.fetchall()

        # Если результат пустой, возвращаем 0
        if not result:
            return 0

        # Разделяем каждую строку по запятой и объединяем в общий список
        url_list = []
        for row in result:
            if row[0]:  # Проверяем, что строка не пустая
                url_list.extend(row[0].split(','))

        # Преобразуем список в множество для удаления дубликатов
        return list(set(url_list))


    #  -------------------------------------------------------------------------------------------Работа с ценами и странами


    def update_price_product(
            country: str,  # Таблица, в которую вносим данные (например, "en-US")
            product_id: str,
            original_price: float,
            discounted_price: float = 0,
            discounted_percentage: float = 0,
            ru_price: float = 0):

        table_name = f'"{country}"'  # Защита от SQL-инъекций (экранирование кавычками)

        # Проверяем, есть ли запись в таблице
        cur.execute(f'SELECT COUNT(*) FROM {table_name} WHERE product_id = ?', (product_id,))
        exists = cur.fetchone()[0] > 0

        if not exists:
            # Если записи нет, создаем новую
            cur.execute(f'INSERT INTO {table_name} (product_id, original_price, discounted_price, discounted_percentage, ru_price) '
                        'VALUES (?, ?, ?, ?, ?)',
                        (product_id, original_price, discounted_price, discounted_percentage, ru_price)
                        )
        else:
            # Если запись уже существует, обновляем
            cur.execute(f'UPDATE {table_name} SET original_price = ?, discounted_price = ?, '
                        'discounted_percentage = ?, ru_price = ? WHERE product_id = ?',
                        (original_price, discounted_price, discounted_percentage, ru_price, product_id)
                        )

        conn.commit()


    def get_product_price(country: str, product_id: str):
        table_name = f'"{country}"'  # Экранируем кавычками для защиты от SQL-инъекций

        # Запрашиваем данные из БД
        cur.execute(f'SELECT original_price, discounted_price, discounted_percentage FROM {table_name} WHERE product_id = ?', (product_id,))
        result = cur.fetchone()

        if result:
            return {
                "original_price": result[0],
                "discounted_price": result[1],
                "discounted_percentage": result[2],
            }
        else:
            return None  # Если товара нет в базе


    def get_exchange():
        cur.execute('SELECT * FROM exchange')
        result = cur.fetchone()
        if result is None:
            return 0

        # Получение имен колонок
        columns = [desc[0] for desc in cur.description]

        # Создание словаря с данными
        exchange_rate = dict(zip(columns, result))

        return exchange_rate


    def get_formulas():
        cur.execute('SELECT * FROM formulas')
        result = cur.fetchone()
        if result is None:
            return 0

        # Получение имен колонок
        columns = [desc[0] for desc in cur.description]

        # Создание словаря с данными
        all_formulas = dict(zip(columns, result))

        return all_formulas


    def get_prices_by_product(product_id):
        prices = {}
        for country, table in regions_id.items():
            cur.execute(f"SELECT * FROM '{table}' WHERE product_id = ?", (product_id,))
            result = cur.fetchall()

            if result:
                columns = [desc[0] for desc in cur.description]
                country_prices = [dict(zip(columns, row)) for row in result]
                prices[country] = country_prices

            else:
                prices[country] = []  # Если нет данных, возвращаем пустой список

        return prices


    def save_ru_price_by_country(product_id: str, country_code: str, ru_price: float):
        # Формируем SQL-запрос с динамическим названием таблицы
        table_name = f'"{country_code}"'  # Берем в кавычки, чтобы избежать ошибок с дефисами
        # Проверяем, есть ли запись с таким product_id
        cur.execute(f'SELECT COUNT(*) FROM {table_name} WHERE product_id = ?', (product_id,))
        exists = cur.fetchone()[0] > 0

        if not exists:
            pass
        else:
            # Если запись уже существует, обновляем цену
            cur.execute(f'UPDATE {table_name} SET ru_price = ? WHERE product_id = ?',
                        (ru_price, product_id))

        conn.commit()


    def save_all_ru_price(product_id: str,
                          min_price_key: int,
                          min_price_your_acc: int,
                          min_price_new_acc: int,
                          discount_percentage: str
                          ):

        cur.execute('''
        CREATE TABLE IF NOT EXISTS minimal_price_game (
            product_id TEXT,
            game_key REAL,
            your_acc REAL,
            new_acc REAL,
            discount_percentage TEXT,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        ''')

        cur.execute(f'SELECT COUNT(*) FROM minimal_price_game WHERE product_id = ?', (product_id,))
        exists = cur.fetchone()[0] > 0

        if not exists:
            # Если записи нет, создаем новую
            cur.execute(f'INSERT INTO minimal_price_game (product_id, game_key, your_acc, new_acc, discount_percentage) '
                        'VALUES (?, ?, ?, ?, ?)',
                        (product_id, min_price_key, min_price_your_acc, min_price_new_acc, discount_percentage)
                        )
        else:
            # Если запись уже существует, обновляем
            cur.execute(f'UPDATE minimal_price_game SET game_key = ?, your_acc = ?, '
                        'new_acc = ?, discount_percentage = ? WHERE product_id = ?',
                        (min_price_key, min_price_your_acc, min_price_new_acc, discount_percentage, product_id)
                        )

        conn.commit()
