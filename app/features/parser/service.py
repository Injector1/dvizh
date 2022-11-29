import asyncio
import threading
import time

import aioschedule as schedule

from app.config import ARTICLES_BY_NAME, TAGS
from app.features.parser.parsers import SportsRUParser, ChampionatParser

from app.features.telegraf import TelegrafService
from app.features.bot import BotService


class ParserService:
    def __init__(self, t_service: TelegrafService, bot_service: BotService):
        self.loop = None
        self.bot_service = bot_service
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
                    if len(ARTICLES_BY_NAME[name]) == 0 or article_info[0] != ARTICLES_BY_NAME[name][0]:
                        ARTICLES_BY_NAME[name].insert(0, article_info)
                        # await self.bot_service.send_all(name, article_info)
        print('done')

    async def start_updating(self, loop):
        self.loop = loop
        await self.update_all_telegraph_articles()
        schedule.every(5).minutes.do(self.update_all_telegraph_articles)
        while True:
            await schedule.run_pending()
            time.sleep(0.1)
