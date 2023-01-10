# - *- coding: utf- 8 - *-
import psycopg2

from config import DB_NAME, HOST, PASSWORD, USER


def is_user(tg_id: int) -> tuple[int]:
    conn = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, dbname=DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT user_id FROM users WHERE tg_id = %s', (tg_id,))
    user_id = cur.fetchone()
    cur.close()
    conn.close()
    return user_id


def add_user(tg_id: int) -> None:
    conn = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, dbname=DB_NAME)
    cur = conn.cursor()
    cur.execute('INSERT INTO users (tg_id) VALUES (%s)', (tg_id,))
    cur.close()
    conn.commit()
    conn.close()
    return


def add_file_path(tg_id: int, file_type: str, file_path: str) -> None:
    conn = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, dbname=DB_NAME)
    cur = conn.cursor()
    user_id = is_user(tg_id)[0]
    cur.execute('INSERT INTO media (user_id, type, file_path) VALUES (%s, %s, %s)', (user_id, file_type, file_path,))
    cur.close()
    conn.commit()
    conn.close()
    return
