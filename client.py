from dependency_injector import containers, providers
from telegraph import Telegraph

from app.features import ParserContainer, UserContainer, TelegrafContainer, BotContainer


class Application(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    telegraf = providers.Singleton(
        Telegraph,
    )

    telegraf_package = providers.Container(
        TelegrafContainer,
        telegraf=telegraf,
        account_name='dvizh'
    )
    parser_package = providers.Container(
        ParserContainer,
        telegraf_service=telegraf_package.telegraf_service
    )
    user_package = providers.Container(
        UserContainer,
    )
    bot_package = providers.Container(
        BotContainer,
        user_repository=user_package.user_repository,
        bot_token=config.bot.bot_token,
    )