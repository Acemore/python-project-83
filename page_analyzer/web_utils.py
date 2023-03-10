import requests
from flask import redirect, url_for
from urllib.parse import urlparse
from validators.url import url as is_correct_url


def get_main_page_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def get_redirect(handler_name, id):
    return redirect(url_for(handler_name, id=id))


def get_status_code_by_url_name(url_name):
    try:
        return requests.get(url_name).status_code
    except requests.RequestException:
        return 0


def validate(url):
    errors = []

    if not url:
        errors.append('URL обязателен')
    elif len(url) > 255:
        errors.append('URL превышает 255 символов')
    elif not is_correct_url(url):
        errors.append('Некорректный URL')

    return errors
