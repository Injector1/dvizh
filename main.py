import asyncio
import threading

from telegraph import Telegraph

from create_schema import database_creation, close_connection
from app.features.parser import ParserService
from app.features.telegraf import TelegrafService, TelegrafModel, JsonRepo
from app.features.bot.bot import NewsBot

from app.features.users.models import UserModel
from app.features.users.users_repo import UserRepo


if __name__ == "__main__":
    telegraph_model = TelegrafModel()
    telegraf_repository = JsonRepo(telegraph_model)
    telegraf_service = TelegrafService(
        telegraf=Telegraph(),
        telegraf_repository=telegraf_repository,
        account_name='dvizh-bot'
    )

    parser_service = ParserService(telegraf_service)

    users_model = UserModel()
    user_repo = UserRepo(users_model)

    try:
        threading.Thread(target=parser_service.start_updating).start()
        b = NewsBot(bot_token='5914366318:AAFihB-KhrA_8-AMX4XuRhwmwHkXgzYEDug', user_repo=user_repo)
        b.add_commands()
    finally:
        asyncio.run(close_connection())
