import requests

from bs4 import BeautifulSoup

from app.features.base import BaseParser
from app.features.telegraf.service import TelegrafService
from app.features.telegraf.schemas import ArticleCreateOrUpdateScheme


class SportsRUParser(BaseParser):
    base_url = 'https://www.sports.ru'

    def __init__(self, telegraf_service: TelegrafService):
        self.telegraf_service = telegraf_service

    def parse(self, tag: str):
        s = BeautifulSoup(requests.get(self.get_url_by_tag(tag)).text, 'html.parser')
        raw_news = s.find_all('a', {'class': 'short-text'})
        return f"{self.base_url}/{raw_news[0]['href']}"

    def get_markdown_view(self, url: str, team_name: str):
        html_view = BeautifulSoup(requests.get(url).text, 'html.parser')
        title = html_view.find_all('header', {'class': 'news-item__header'})[0].find_all_next('h1')[0].text[1:-1]
        page = html_view.find_all('div', {'class': 'news-item__content'})
        page_text = [(p.text + '\n') for p in page][0]
        article = ArticleCreateOrUpdateScheme(title=title, content=page_text, team_name=team_name)
        href = self.telegraf_service.create_telegraf_article(article)
        return title, href

    def get_html_view(self, url: str):
        return BeautifulSoup(requests.get(url).text, 'html.parser')

    def get_url_by_tag(self, tag: str) -> str:
        return f'{self.base_url}/{tag}/news/'
