from telegraph import Telegraph
from time import localtime

from .schemas import ArticleCreateOrUpdateScheme, TelegrafCreateOrUpdateScheme
from .repository import TelegrafRepository


class TelegrafService:
    def __init__(
            self,
            telegraf: Telegraph,
            telegraf_repository: TelegrafRepository,
            account_name: str):
        self.telegraf = telegraf
        self.telegraf_repository = telegraf_repository
        self.telegraf.create_account(short_name=account_name)

    def create_telegraf_article(self, article: ArticleCreateOrUpdateScheme):
        body = [i + '\n\n' for i in article.content.split('\n')]
        response = self.telegraf.create_page(
            title=article.title,
            author_name=f'DVIZH•{localtime().tm_hour} : {localtime().tm_min}',
            content=body,
            html_content=None
        )
        telegraf_article = TelegrafCreateOrUpdateScheme(
            title=article.title,
            url=f'https://telegra.ph/{response["path"]}',
            team_name=article.team_name
        )
        self.telegraf_repository.create(telegraf_article)
        return telegraf_article.url
