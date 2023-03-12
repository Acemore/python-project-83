import os
import psycopg2
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from .db import (
    add_url,
    create_url_check,
    get_url_by_id,
    get_url_by_url_name,
    get_url_checks_by_url_id,
    get_urls_and_last_checks_data,
)
from .web_utils import (
    get_main_page_url,
    get_status_code_by_url_name,
    validate,
)

load_dotenv()

app = Flask(__name__)

app.database_url = os.getenv('DATABASE_URL')
app.secret_key = os.getenv('SECRET_KEY')

conn = psycopg2.connect(app.database_url)


def get_redirect_to_url_details_page(id):
    return redirect(url_for('get_url_details', id=id))


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'index.html',
        messages=messages,
    )


@app.get('/urls')
def urls_show():
    data = get_urls_and_last_checks_data(conn)

    return render_template(
        'urls/index.html',
        data=data,
    )


@app.post('/urls')
def post_url():
    url_name = request.form.get('url')

    errors = validate(url_name)
    if errors:
        for error in errors:
            flash(error, 'danger')

        return render_template(
            'index.html',
            url_name=url_name,
            messages=get_flashed_messages(with_categories=True),
        ), 422

    url_name = get_main_page_url(url_name)
    url = get_url_by_url_name(conn, url_name)

    if url:
        flash('Страница уже существует', 'info')
        id = url.id
    else:
        id = add_url(conn, url_name)
        flash('Страница успешно добавлена', 'success')

    return get_redirect_to_url_details_page(id)


@app.get('/urls/<int:id>')
def get_url_details(id):
    return render_template(
        'urls/url.html',
        url=get_url_by_id(conn, id),
        url_checks=get_url_checks_by_url_id(conn, id),
        messages=get_flashed_messages(with_categories=True),
    )


@app.post('/urls/<int:id>/checks')
def post_url_check(id):
    url = get_url_by_id(conn, id)
    status_code = get_status_code_by_url_name(url.name)

    if status_code and status_code < 400:
        create_url_check(conn, url, status_code)
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return get_redirect_to_url_details_page(id)
