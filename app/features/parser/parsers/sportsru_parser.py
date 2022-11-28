import requests

from bs4 import BeautifulSoup
from typing import Tuple

from app.features.base import BaseParser
from app.features.telegraf.service import TelegrafService
from app.features.telegraf.schemas import ArticleCreateOrUpdateScheme


class SportsRUParser(BaseParser):
    base_url = 'https://www.sports.ru'

    def __init__(self, telegraf_service: TelegrafService):
        self.telegraf_service = telegraf_service

    def parse(self, html: BeautifulSoup) -> Tuple[str, str]:
        title = html.find_all('header', {'class': 'news-item__header'})[0].find_all_next('h1')[0].text[1:-1]
        page = html.find_all('div', {'class': 'news-item__content'})
        page_text = [(p.text + '\n') for p in page][0]
        return title, page_text

    async def get_markdown_view(self, tag: str, team_name: str):
        html_view = self.get_html_view(self.get_url_by_tag(tag))
        title, page_text = self.parse(html_view)
        article = ArticleCreateOrUpdateScheme(title=title, content=page_text, team_name=team_name)
        href = await self.telegraf_service.create_telegraf_article(article)
        return title, href

    def get_html_view(self, url: str) -> type(BeautifulSoup):
        return BeautifulSoup(requests.get(url).text, 'html.parser')

    def get_url_by_tag(self, tag: str) -> str:
        s = self.get_html_view(f'{self.base_url}/{tag}/news/')
        raw_news = s.find_all('a', {'class': 'short-text'})
        return f"{self.base_url}/{raw_news[0]['href']}"
