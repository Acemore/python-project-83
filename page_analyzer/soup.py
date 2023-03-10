import requests
from bs4 import BeautifulSoup


def get_tags_data(url_name):
    resp = requests.get(url_name)
    soup = BeautifulSoup(resp.text, 'html.parser')

    if (h1_tag := soup.h1):
        h1 = h1_tag.text
    else:
        h1 = ''
    # h1 = h1_tag.text if (h1_tag := soup.h1) else ''
    if (title_tag := soup.title):
        title = title_tag.text
    else:
        title = ''
    # title = title_tag.text if (title_tag := soup.title) else ''
    if (meta_tag := soup.find('meta', attrs={'name': 'description'})):
        description = meta_tag.get('content')
    else:
        description = ''
    # description = meta_tag.get('content') if (
        # meta_tag := soup.find('meta', attrs={'name': 'description'})
    # ) else ''

    return {
        'h1': h1,
        'title': title,
        'description': description,
    }
