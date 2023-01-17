from dependency_injector import containers, providers
from aiogram import Dispatcher

from .bot import NewsBot


class BotContainer(containers.DeclarativeContainer):
    bot = providers.Dependency()
    user_repository = providers.Dependency()
    article_repository = providers.Dependency()

    dispatcher = providers.Singleton(
        Dispatcher,
        bot=bot
    )

    news_bot = providers.Singleton(
        NewsBot,
        bot=bot,
        dp=dispatcher,
        user_repository=user_repository,
        article_repository=article_repository
    )

