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
from itertools import zip_longest

from .db import (
    create_url_check,
    get_last_url_check,
    get_url_by_id,
    get_url_checks_by_url_id,
    get_url_id_by_url_name,
    get_urls,
)
from .urls import normalize_url, validate

load_dotenv()

app = Flask(__name__)

app.database_url = os.getenv('DATABASE_URL')
app.secret_key = os.getenv('SECRET_KEY')

conn = psycopg2.connect(app.database_url)


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)

    return render_template(
        'index.html',
        messages=messages,
    )


@app.get('/urls')
def urls_show():
    urls = get_urls(conn)
    last_url_checks = [get_last_url_check(conn, url) for url in urls]

    return render_template(
        'urls/index.html',
        data=zip_longest(urls, last_url_checks),
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

    normalized_url_name = normalize_url(url_name)
    url_id = get_url_id_by_url_name(conn, normalized_url_name)

    return redirect(url_for('get_url_details', id=url_id))


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
    create_url_check(conn, url)

    return redirect(url_for('get_url_details', id=id))
