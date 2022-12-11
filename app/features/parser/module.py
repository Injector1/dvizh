from dependency_injector import containers, providers


from .parsers import ChampionatParser, SportsRUParser
from .service import ParserService


class ParserContainer(containers.DeclarativeContainer):
    telegraf_service = providers.Dependency()

    championat_parser = providers.Singleton(
        ChampionatParser,
        telegraf_service=telegraf_service
    )
    sportsru_parser = providers.Singleton(
        SportsRUParser,
        telegraf_service=telegraf_service
    )

    parser_service = providers.Singleton(
        ParserService,
        parsers=providers.List(sportsru_parser, championat_parser)
    )

