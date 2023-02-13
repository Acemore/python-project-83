from flask import flash
from psycopg2.extras import NamedTupleCursor


def get_url_by_id(conn, url_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE id = %s;', (url_id,))
        url = curs.fetchone()

    return url


def get_url_id_by_url_name(conn, url_name):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT * FROM urls WHERE name = %s;', (url_name,))
        url_in_list_to_check = curs.fetchone()

        if url_in_list_to_check:
            flash('Страница уже существует', 'info')
            id = url_in_list_to_check.id
        else:
            curs.execute('INSERT INTO urls (name) VALUES (%s) RETURNING id', (url_name,))
            id, = curs.fetchone()
            conn.commit()
            flash('Страница успешно добавлена', 'success')

    return id


def get_urls(conn):
    with conn.cursor() as curs:
        curs.execute('SELECT * FROM urls ORDER BY id DESC;')
        urls = curs.fetchall()

    return urls
