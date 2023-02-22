import requests


def get_status_code_by_url_name(url_name):
    try:
        return requests.get(url_name).status_code
    except requests.RequestException:
        return 404
