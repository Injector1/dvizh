from app.config import ARTICLES_BY_NAME, TAGS
from .parsers.sportsru_parser import SportsRUParser
import schedule


METHOD_BY_SITE = {'sports.ru': SportsRUParser}


def update_all_telegraph_articles():
    print('start')
    for name in ARTICLES_BY_NAME.keys():
        print(f'Updating team {name}')
        for site, tag in TAGS[name].items():
            if site in METHOD_BY_SITE.keys():
                cl = METHOD_BY_SITE[site]()
                article_info = cl.get_markdown_view(cl.parse(tag))
                ARTICLES_BY_NAME[name][0] = article_info
    print('done')


def start_updating():
    update_all_telegraph_articles()
    schedule.every(5).minutes.do(update_all_telegraph_articles)
    while True:
        schedule.run_pending()
