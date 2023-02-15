import requests
from flask import flash
from psycopg2.extras import NamedTupleCursor

from .soup import get_tags_data


def create_url_check(conn, url):
    status_code = get_status_code_by_url_name(url.name)

    if status_code:
        tags_data = get_tags_data(url.name)
        with conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(
                    'INSERT INTO url_checks\
                    (url_id, status_code, h1, title, description, created_at)\
                    VALUES (%s, %s, %s, %s, %s, %s);',
                    (
                        url.id,
                        status_code,
                        tags_data['h1'],
                        tags_data['title'],
                        tags_data['description'],
                        url.created_at,
                    ),
                )
                conn.commit()

        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')


def get_last_url_check(conn, url):
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                'SELECT *\
                FROM url_checks\
                WHERE url_id = %s\
                ORDER BY id DESC;',
                (url.id,),
            )
            last_check = curs.fetchone()

    return last_check


def get_status_code_by_url_name(url_name):
    try:
        return requests.get(url_name).status_code
    except requests.RequestException:
        return


def get_url_by_id(conn, url_id):
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                'SELECT * FROM urls WHERE id = %s;',
                (url_id,),
            )
            url = curs.fetchone()

    return url


def get_url_checks_by_url_id(conn, url_id):
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                'SELECT *\
                FROM url_checks\
                WHERE url_id = %s\
                ORDER BY id DESC;',
                (url_id,),
            )
            url_checks = curs.fetchall()

    return url_checks


def get_url_id_by_url_name(conn, url_name):
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(
                'SELECT * FROM urls WHERE name = %s;',
                (url_name,),
            )
            url_in_list_to_check = curs.fetchone()

            if url_in_list_to_check:
                flash('Страница уже существует', 'info')
                id = url_in_list_to_check.id
            else:
                curs.execute(
                    'INSERT INTO urls (name) VALUES (%s) RETURNING id',
                    (url_name,),
                )
                id, = curs.fetchone()
                conn.commit()
                flash('Страница успешно добавлена', 'success')

    return id


def get_urls(conn):
    with conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute('SELECT * FROM urls ORDER BY id DESC;')
            urls = curs.fetchall()

    return urls
