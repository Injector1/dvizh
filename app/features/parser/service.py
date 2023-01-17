import asyncio
import re
import time
from typing import Iterable, Dict

import aioschedule as schedule

from app.config import ARTICLES_BY_NAME, TAGS
from app.features.base import BaseParser
from app.features.bot.service import BotService


class ParserService:
    def __init__(
            self,
            parsers: Iterable[BaseParser]):
        self.parsers = parsers
        self.mapped_parsers = self.map_parsers()

    def map_parsers(self) -> Dict[str, BaseParser]:
        url = re.compile(r"https?://(www\.)?")
        return {url.sub('', parser.base_url).strip().strip('/'): parser for parser in self.parsers}

    async def update_all_telegraph_articles(self):
        print('start')
        for name in ARTICLES_BY_NAME.keys():
            for site, tag in TAGS[name].items():
                if site in self.mapped_parsers.keys():
                    print(f'Updating {name} via {site}...')
                    try:
                        article_info = await self.mapped_parsers[site].get_markdown_view(tag, name)
                        if len(ARTICLES_BY_NAME[name]) == 0 or article_info[0] != ARTICLES_BY_NAME[name][0]:
                            ARTICLES_BY_NAME[name].insert(0, article_info)
                    except:
                        pass
        print('done')

    async def start_updating(self):
        await self.update_all_telegraph_articles()
        schedule.every(5).minutes.do(self.update_all_telegraph_articles)
        while True:
            #await self.update_all_telegraph_articles()
            await schedule.run_pending()
            time.sleep(5000)
