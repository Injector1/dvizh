import asyncio
import threading

from dependency_injector.wiring import Provide, inject


from client import Application
from app.features.bot.bot import NewsBot
from app.features.bot import BotService

from app.features.users.models import UserModel
from app.features.users.users_repo import UserRepo


def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(parser_service.start_updating(loop))
    loop.close()


if __name__ == "__main__":
    telegraph_model = TelegrafModel()
    telegraf_repository = JsonRepo(telegraph_model)
    telegraf_service = TelegrafService(
        telegraf=Telegraph(),
        telegraf_repository=telegraf_repository,
        account_name='dvizh-bot'
    )
from app.features import ParserService

    users_model = UserModel()
    user_repo = UserRepo(users_model)
    b = NewsBot(
        bot_token='5914366318:AAFihB-KhrA_8-AMX4XuRhwmwHkXgzYEDug',
        user_repo=user_repo,
        article_repo=telegraf_repository
    )

    bot_service = BotService(bot=b)
    parser_service = ParserService(telegraf_service, bot_service)


@inject
def main(
        parser_service: ParserService = Provide[
            Application.parser_package.parser_service
        ],
        bot: NewsBot = Provide[
            Application.bot_package.bot
        ]
):
    try:
        threading.Thread(target=between_callback).start()
        b.add_commands()
        threading.Thread(target=parser_service.start_updating).start()
        bot.add_commands()
    finally:
        # asyncio.run(close_connection())
        print(123)


if __name__ == "__main__":
    application = Application()
    application.wire(modules=[__name__])
    main()
