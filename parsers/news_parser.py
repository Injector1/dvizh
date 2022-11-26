import requests
from bs4 import BeautifulSoup
from random import choice
import schedule
from .page_maker import get_page


URL = 'https://www.sports.ru'
ARTICLES_BY_NAME = {
    'Барселона': [],
    'Реал Мадрид': [],
    'Атлетико Мадрид': [],
    'Ювентус': [],
    'Милан': [],
    'Интер Милан': [],
    'Наполи': [],
    'Лацио': [],
    'Торино': [],
    'Аталанта': [],
    'Рома': [],
    'Фиорентина': [],
    'Арсенал': [],
    'Манчестер Сити': [],
    'Тоттенхэм': [],
    'Ливерпуль': [],
    'Арсенал': [],
    'Манчестер Юнайтед': [],
    'Челси': [],
    'ПСЖ': [],
    'Зенит': [],
    'Спартак Москва': [],
    'Локомотв Москва': [],
    'Урал': [],
    'Динамо Москва': [],
    'Крылья Советов': [],
    'Ростов': []
}
TAGS = {
    'Барселона': {
        'sports.ru': 'barselona',
        'championat.com': '552-fk-barselona'
    },
    'Реал Мадрид': {
        'sports.ru': 'real',
        'championat.com': '551-fk-real-madrid'
    },
    'Атлетико Мадрид': {
        'sports.ru': 'atletico',
        'championat.com': '597-atletiko-madrid'
    },
    'Ювентус': {
        'sports.ru': 'juventus',
        'championat.com': '555-juventus'
    },
    'Милан': {
        'sports.ru': 'milan',
        'championat.com': '556-fk-milan'
    },
    'Интер Милан': {
        'sports.ru': 'inter',
        'championat.com': '553-inter'
    },
    'Наполи': {
        'sports.ru': 'napoli',
        'championat.com': '607-napoli'
    },
    'Лацио': {
        'sports.ru': 'lazio',
        'championat.com': '1044-lacio'
    },
    'Торино': {
        'sports.ru': 'torino',
        'championat.com': '775-torino'
    },
    'Аталанта': {
        'sports.ru': 'atalanta',
        'championat.com': '1241-atalanta'
    },
    'Рома': {
        'sports.ru': 'roma',
        'championat.com': '554-roma'
    },
    'Фиорентина': {
        'sports.ru': 'fiorentina',
        'championat.com': '764-fiorentina'
    },
    'Бавария': {
        'sports.ru': 'bayern',
        'championat.com': '557-bavarija'
    },
    'Боруссия Дортмунд': {
        'sports.ru': 'borussia',
        'championat.com': '1169-borussija-d'
    },
    'Арсенал': {
        'sports.ru': 'arsenal',
        'championat.com': '548-arsenal'
    },
    'Манчестер Сити': {
        'sports.ru': 'manchester-city',
        'championat.com': '602-manchester-siti'
    },
    'Тоттенхэм': {
        'sports.ru': 'tottenham',
        'championat.com': '550-tottenkhjem'
    },
    'Ливерпуль': {
        'sports.ru': 'liverpool',
        'championat.com': '549-liverpul'
    },
    'Манчестер Юнайтед': {
        'sports.ru': 'mu',
        'championat.com': '546-manchester-junajted'
    },
    'Челси': {
        'sports.ru': 'chelsea',
        'championat.com': '547-chelsi'
    },
    'ПСЖ': {
        'sports.ru': 'psg',
        'championat.com': '684-pszh'
    },
    'Зенит': {
        'sports.ru': 'zenit',
        'championat.com': '5-fk-zenit'
    },
    'Спартак Москва': {
        'sports.ru': 'spartak',
        'championat.com': '1-fk-spartak'
    },
    'Локомотв Москва': {
        'sports.ru': 'lokomotiv',
        'championat.com': '3-fk-lokomotiv'
    },
    'Урал': {
        'sports.ru': 'ural',
        'championat.com': '741-fk-ural'
    },
    'Динамо Москва': {
        'sports.ru': 'dynamo',
        'championat.com': '4-fk-dinamo-moskva'
    },
    'Крылья Советов': {
        'sports.ru': 'krylia-sovetov',
        'championat.com': '14-fk-krylja-sovetov'
    },
    'Ростов': {
        'sports.ru': 'rostov',
        'championat.com': '6-fk-rostov'
    },
    'ЦСКА': {
        'sports.ru': 'cska',
        'championat.com': '2-pfk-cska'
    },
    'Краснодар': {
        'sports.ru': 'krasnodar',
        'championat.com': '885-krasnodar'
    }
}


def get_url(name):
    tag = TAGS[name]['sports.ru']
    return f'{URL}/{tag}/news/'


def get_article_urls_by_name(name: str, n: int) -> list[str]:
    s = BeautifulSoup(requests.get(get_url(name)).text, 'html.parser')
    raw_news = s.find_all('a', {'class': 'short-text'})
    return [f"{URL}/{raw_news[i]['href']}" for i in range(min(n, len(raw_news) - 1))]


def article_url_to_telegraph(url) -> tuple[str, str]:
    s = BeautifulSoup(requests.get(url).text, 'html.parser')
    title = s.find_all('header', {'class': 'news-item__header'})[0].find_all_next('h1')[0].text[1:-1]
    page = s.find_all('div', {'class': 'news-item__content'})
    page_text = [(p.text + '\n') for p in page][0]
    href = get_page(title, page_text)
    return title, href


def is_item_in_sequence(item:str, m: list[(str, str)]) -> bool:
    return any(item == title for title, _ in m)


def update_all_telegraph_articles():
    print('start')
    for name in ARTICLES_BY_NAME.keys():
        article_urls = get_article_urls_by_name(name, 15)
        for article_url in article_urls:
            article_info = article_url_to_telegraph(article_url)
            if not is_item_in_sequence(article_info[0], ARTICLES_BY_NAME[name]):
                ARTICLES_BY_NAME[name].append(article_info)
                print(article_info)
            else:
                print('Nothing changes')
    print('done')


def get_random_news(name: str) -> tuple[str, str]:
    return choice(ARTICLES_BY_NAME[name])


def get_latest_news(name: str) -> tuple[str, str]:
    return ARTICLES_BY_NAME[name][0]


def start_updating():
    update_all_telegraph_articles()
    schedule.every(5).minutes.do(update_all_telegraph_articles)
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    start_updating()
