import threading

from telegraph import Telegraph

from app.features.parser import ParserService, SportsRUParser
from app.features.telegraf import TelegrafService, TelegrafRepository
from app.features.bot.bot import NewsBot


if __name__ == "__main__":
    telegraf_repository = TelegrafRepository()
    telegraf_service = TelegrafService(
        telegraf=Telegraph(),
        telegraf_repository=telegraf_repository,
        account_name='dvizh-bot'
    )
    parser_service = ParserService(
        SportsRUParser(
            telegraf_service=telegraf_service
        )
    )
    thr1 = threading.Thread(target=parser_service.start_updating).start()
    b = NewsBot(bot_token='5914366318:AAFihB-KhrA_8-AMX4XuRhwmwHkXgzYEDug')
    b.add_commands()