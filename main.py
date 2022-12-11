import asyncio
import threading

from dependency_injector.wiring import Provide, inject

from client import Application
from app.features.bot.bot import NewsBot
from app.features.parser import ParserService


@inject
def between_callback(
        parser_service: ParserService = Provide[
            Application.parser_package.parser_service
        ]):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(parser_service.start_updating(loop))
    loop.close()


@inject
def main(
        bot: NewsBot = Provide[
            Application.bot_package.news_bot
        ]
):
    try:
        threading.Thread(target=between_callback).start()
        bot.add_commands()
    finally:
        print(123)


if __name__ == "__main__":
    application = Application()
    application.wire(modules=[__name__])
    main()
