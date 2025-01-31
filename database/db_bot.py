import sqlite3

relative_path = "db_bot.db"

conn = sqlite3.connect(relative_path)
cur = conn.cursor()


async def start_db():
    cur.execute("""CREATE TABLE IF NOT EXISTS config(
        date_auto_pars_sale TEXT,
        time_auto_pars_sale TEXT,
        date_auto_pars_products TEXT,
        time_auto_pars_products TEXT,
        date_auto_pars_new_products TEXT,
        time_auto_pars_new_products TEXT
        )
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS country(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        "IN" BOOL DEFAULT 0,
        NG BOOl DEFAULT 0,
        US BOOl DEFAULT 0,
        AR BOOl DEFAULT 0,
        TR BOOl DEFAULT 0,
        UA BOOl DEFAULT 0
        )
        """)

    # Проверяем, есть ли записи в таблице country
    cur.execute("SELECT COUNT(*) FROM country")
    count = cur.fetchone()[0]

    # Если записей нет, добавляем начальную строку
    if count == 0:
        cur.execute("""
                INSERT INTO country ("IN", NG, US, AR, TR, UA)
                VALUES (0, 0, 0, 0, 0, 0)
            """)

    # Сохраняем изменения
    conn.commit()


def get_all_county_pars():
    cur.execute('SELECT * FROM country')
    row = cur.fetchall()[0]
    return {
        "IN": row[1],
        "NG": row[2],
        "US": row[3],
        "AR": row[4],
        "TR": row[5],
        "UA": row[6],
    }


def update_region_pars(region: str, status: int):
    # Используем параметризованный запрос для безопасности
    query = f'UPDATE country SET "{region}" = ?'
    cur.execute(query, (status,))
    conn.commit()