from urllib.parse import urlparse
from validators.url import url as is_correct_url


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def validate(url):
    errors = []

    if not url:
        errors.append('URL обязателен')
    elif len(url) > 255:
        errors.append('URL превышает 255 символов')
    elif not is_correct_url(url):
        errors.append('Некорректный URL')

    return errors
