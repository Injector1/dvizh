import asyncio
import threading

from telegraph import Telegraph

from create_schema import database_creation, close_connection
from app.features.parser import ParserService, SportsRUParser, ChampionatParser
from app.features.telegraf import TelegrafService, TelegrafModel, JsonRepo
from app.features.bot.bot import NewsBot


if __name__ == "__main__":
    telegraph_model = TelegrafModel()
    telegraf_repository = JsonRepo(telegraph_model)
    telegraf_service = TelegrafService(
        telegraf=Telegraph(),
        telegraf_repository=telegraf_repository,
        account_name='dvizh-bot'
    )

    parser_service = ParserService(telegraf_service)

    # loop = asyncio.get_event_loop()
    try:
        '''
        # loop.run_until_complete(database_creation())
        print(asyncio.run(TelegrafModel.create(
            title='sdfsdf',
            telegraf_url='sdf',
            team_name='sd'
        )))
        parser_service.start_updating()
        '''
        thr1 = threading.Thread(target=parser_service.start_updating).start()
        b = NewsBot(bot_token='5914366318:AAFihB-KhrA_8-AMX4XuRhwmwHkXgzYEDug')
        b.add_commands()
    finally:
        asyncio.run(close_connection())
