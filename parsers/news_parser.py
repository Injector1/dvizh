import requests
from bs4 import BeautifulSoup
import schedule
from .page_maker import get_page
from app.config.teams import TAGS, ARTICLES_BY_NAME


URL = 'https://www.sports.ru'


def get_url(name):
    tag = TAGS[name]['sports.ru']
    return f'{URL}/{tag}/news/'


def get_article_urls_by_name(name: str) -> str:
    s = BeautifulSoup(requests.get(get_url(name)).text, 'html.parser')
    raw_news = s.find_all('a', {'class': 'short-text'})
    return f"{URL}/{raw_news[0]['href']}"


def article_url_to_telegraph(url) -> tuple[str, str]:
    s = BeautifulSoup(requests.get(url).text, 'html.parser')
    title = s.find_all('header', {'class': 'news-item__header'})[0].find_all_next('h1')[0].text[1:-1]
    page = s.find_all('div', {'class': 'news-item__content'})
    page_text = [(p.text + '\n') for p in page][0]
    href = get_page(title, page_text)
    return title, href


def get_latest_news(name: str) -> tuple[str, str]:
    return ARTICLES_BY_NAME[name][0]


def update_all_telegraph_articles():
    print('start')
    for name in ARTICLES_BY_NAME.keys():
        article_url = get_article_urls_by_name(name)
        article_info = article_url_to_telegraph(article_url)
        if article_info[0] != ARTICLES_BY_NAME[name][0]:
            ARTICLES_BY_NAME[name] = article_info
            print(article_info)
        else:
            print('Nothing changes')
    print('done')


def start_updating():
    update_all_telegraph_articles()
    schedule.every(5).minutes.do(update_all_telegraph_articles)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    start_updating()
