from urllib.parse import urlparse
from validators.url import url as is_correct_url


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def validate(url):
    errors = []

    if len(url) > 255:
        errors.append('URL превышает 255 символов')
    if not is_correct_url(url):
        errors.append('Некорректный URL')
    if not url:
        errors.append('URL обязателен')

    return errors
