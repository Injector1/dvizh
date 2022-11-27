from app.config import ARTICLES_BY_NAME, TAGS
from .parsers.sportsru_parser import SportsRUParser
import schedule


METHOD_BY_SITE = {'sports.ru': SportsRUParser}


class ParserService:
    def __init__(self, sportsru_parser: SportsRUParser):
        self.sportsru_parser = sportsru_parser

    def update_all_telegraph_articles(self):
        print('start')
        for name in ARTICLES_BY_NAME.keys():
            print(f'Updating team {name}')
            for site, tag in TAGS[name].items():
                if site in METHOD_BY_SITE.keys():
                    article_info = self.sportsru_parser.get_markdown_view(
                        self.sportsru_parser.parse(tag),
                        name
                    )
                    ARTICLES_BY_NAME[name][0] = article_info
        print('done')

    def start_updating(self):
        self.update_all_telegraph_articles()
        schedule.every(5).minutes.do(self.update_all_telegraph_articles)
        while True:
            schedule.run_pending()
