import asyncio
import threading
from time import sleep

from dependency_injector.wiring import Provide, inject

from client import Application
from app.features.bot.bot import NewsBot
from app.features.parser import ParserService
from app.features.bot.service import BotService


@inject
def notify_callback(bot: NewsBot):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(BotService(bot).start_schedule())
    loop.close()


@inject
def updating_news_callback(
        parser_service: ParserService = Provide[
            Application.parser_package.parser_service
        ]):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(parser_service.start_updating())
    loop.close()


@inject
def bot_callback(bot):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.add_commands())
    loop.close()


@inject
def main(
    bot: NewsBot = Provide[
        Application.bot_package.news_bot
    ]):
    try:
        th = threading.Thread(target=bot_callback, args=(bot,))
        th.start()

        news_updater_thread = threading.Thread(target=updating_news_callback)
        news_updater_thread.start()
        news_updater_thread.join()

        notify_thread = threading.Thread(target=notify_callback, args=(bot,))
        notify_thread.start()
        notify_thread.join()
    finally:
        print("Jobs done")


if __name__ == "__main__":
    application = Application()
    application.wire(modules=[__name__])
    main()
