import requests
from bs4 import BeautifulSoup


def get_tags_data(url_name):
    resp = requests.get(url_name)
    soup = BeautifulSoup(resp.text, 'html.parser')

    h1 = soup.h1.text if soup.h1 else ''
    title = soup.title.text if soup.title else ''
    description = soup.find('meta', attrs={'name': 'description'}).get("content") if soup.find('meta', attrs={'name': 'description'}) else ''

    tags_data = {
        'h1': h1,
        'title': title,
        'description': description,
    }

    return tags_data
