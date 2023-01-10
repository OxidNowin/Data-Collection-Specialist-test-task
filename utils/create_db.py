# - *- coding: utf- 8 - *-
import psycopg2
from config import DB_NAME, HOST, PASSWORD, USER


def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            tg_id BIGINT UNIQUE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS media (
            media_id SERIAL PRIMARY KEY,
            user_id INTEGER,
            type VARCHAR(255),
            file_path VARCHAR (255),
            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
    )

    conn = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, dbname=DB_NAME)
    cur = conn.cursor()
    for com in commands:
        cur.execute(com)
    conn.commit()
    cur.close()
    conn.close()
