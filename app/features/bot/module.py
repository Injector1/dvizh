from dependency_injector import containers, providers

from .bot import NewsBot


class BotContainer(containers.DeclarativeContainer):
    user_repository = providers.Dependency()
    bot_token = providers.Dependency()

    bot = providers.Singleton(
        NewsBot,
        bot_token=bot_token,
        user_repo=user_repository
    )

