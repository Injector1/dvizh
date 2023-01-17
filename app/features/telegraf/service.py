from telegraph import Telegraph
from tortoise import run_async
import datetime

from .schemas import ArticleCreateOrUpdateScheme, TelegrafCreateOrUpdateScheme
from .repository import TelegrafRepository
from .json_repo import JsonRepository


class TelegrafService:
    def __init__(
            self,
            telegraf: Telegraph,
            telegraf_repository: [TelegrafRepository, JsonRepository],
            account_name: str):
        self.telegraf = telegraf
        self.telegraf_repository = telegraf_repository
        self.telegraf.create_account(short_name=account_name)

    async def create_telegraf_article(self, article: ArticleCreateOrUpdateScheme, origin: str):
        body = [i + '\n\n' for i in article.content.split('\n')]
        body.append(f'{str(datetime.datetime.now())[:16]}')  # TODO: брать с сайта
        body.append(f'\n{origin}')
        response = self.telegraf.create_page(
            title=article.title,
            author_name=f'DVIZH',
            content=body,
            html_content=None
        )
        telegraf_article = await self.telegraf_repository.create(
            TelegrafCreateOrUpdateScheme(
                title=article.title,
                url=f'https://telegra.ph/{response["path"]}',
                team_name=article.team_name
            )
        )
        return telegraf_article.url
