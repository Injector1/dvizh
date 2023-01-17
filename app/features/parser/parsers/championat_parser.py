import requests

from bs4 import BeautifulSoup
from typing import Tuple

from app.features.base import BaseParser
from app.features.telegraf.service import TelegrafService
from app.features.telegraf.schemas import ArticleCreateOrUpdateScheme


class ChampionatParser(BaseParser):
    base_url = 'https://www.championat.com'

    def __init__(self, telegraf_service: TelegrafService):
        self.telegraf_service = telegraf_service

    def parse(self, html: BeautifulSoup) -> Tuple[str, str]:
        title = html.find_all('div', {'class': 'article-head__title'})[0].text
        page_text = ''.join(
            f"{p.text}\n" for p in html.find('div', {'class': 'article-content'}).find_all('p', {'class': ''})
        )

        return title, page_text

    async def get_markdown_view(self, tag: str, team_name: str):
        article_url = self.get_url_by_tag(tag)
        html_view = self.get_html_view(article_url)
        title, page_text = self.parse(html_view)
        article = ArticleCreateOrUpdateScheme(title=title, content=page_text, team_name=team_name)
        href = await self.telegraf_service.create_telegraf_article(article, article_url)
        return title, href

    def get_html_view(self, url: str) -> type(BeautifulSoup):
        headers = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        return BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')

    def get_url_by_tag(self, tag: str) -> str:
        s = self.get_html_view(f'{self.base_url}/tags/{tag}/news/')
        raw_news = s.find_all('a', {'class': 'news-item__title'})
        get_hot_topic = False
        return f"{self.base_url}/{raw_news[0 if get_hot_topic else 1]['href']}"
