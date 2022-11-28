import asyncio
import time

import aioschedule as schedule

from app.config import ARTICLES_BY_NAME, TAGS
from app.features.parser.parsers import SportsRUParser, ChampionatParser

from app.features.telegraf import TelegrafService


class ParserService:
    def __init__(self, t_service: TelegrafService):
        self.method_by_site = {
            'sports.ru': SportsRUParser(t_service),
            'championat.com': ChampionatParser(t_service)
        }

    async def update_all_telegraph_articles(self):
        print('start')
        for name in ARTICLES_BY_NAME.keys():
            for site, tag in TAGS[name].items():
                if site in self.method_by_site.keys():
                    print(f'Updating {name} via {site}...')
                    article_info = await self.method_by_site[site].get_markdown_view(tag, name)
                    ARTICLES_BY_NAME[name].append(article_info)
                    # if ARTICLES_BY_NAME[name][0] != article_info[0]:
                    #    print(f'Change: {ARTICLES_BY_NAME[name][0]} -> {article_info[0]}')
                    #  ARTICLES_BY_NAME[name][0] = article_info
        print('done')

    def start_updating(self):
        asyncio.run(self.update_all_telegraph_articles())
        schedule.every(5).minutes.do(self.update_all_telegraph_articles)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            loop.run_until_complete(schedule.run_pending())
            time.sleep(0.1)
