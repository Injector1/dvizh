from aiogram import executor, types
from database import get_from_database, add_to_database
from app.features.parser import start_updating
from app.config import ARTICLES_BY_NAME
from app.features.parser.parsers import SportsRUParser
import threading
import logging
from aiogram import Bot, Dispatcher


class NewsBot:
    def __init__(self):
        self.parser = SportsRUParser()
        token = '5914366318:AAFihB-KhrA_8-AMX4XuRhwmwHkXgzYEDug'
        bot = Bot(token=token)
        self.dp = Dispatcher(bot)
        logging.basicConfig(level=logging.INFO)

    def add_commands(self) -> None:
        commands = [
            (self.add_team, ['set']),
            (self.get_team, ['get']),
            (self.send_news, ['news'])
        ]
        for command in commands:
            self.dp.register_message_handler(command[0], commands=command[1])
        executor.start_polling(self.dp, skip_updates=True)

    async def add_team(self, message: types.Message):
        try:
            username, team = message.chat['username'], message.text.split()[1]
        except IndexError:
            await message.answer(f'Неверный формат. Попробуйте\n/set <название_команды>')
            return
        add_to_database(username, team)
        await message.answer(f'Пользователю {username} успешно '
                             f'была присвоена команда {team}.')

    async def get_team(self, message: types.Message):
        username = message.chat['username']
        data = get_from_database()
        if username in data.keys():
            await message.answer(f'Для пользователя {username} '
                                 f'зарегистрирована команда {data[username]}')
        else:
            await message.answer(f'Для пользователя {username} не '
                                 f'зарегистрирована команда. Это можно сделать '
                                 f'с помощью команды /set <название_команды>')

    async def send_news(self, message: types.Message):
        data = get_from_database()
        user = message.chat['username']
        if user in data.keys():
            team = data[user]
        else:
            await message.answer(f'Для пользователя {user} не '
                                 f'зарегистрирована команда. Это можно сделать '
                                 f'с помощью команды /set <название_команды>')
            return
        if team not in ARTICLES_BY_NAME.keys():
            await message.answer('Неизвестная футбольная команда')
            return
        title, href = ARTICLES_BY_NAME[team][0]
        await message.answer(f'[{title}]({href})', parse_mode='Markdown')


if __name__ == "__main__":
    thr1 = threading.Thread(target=start_updating).start()
    b = NewsBot()
    b.add_commands()
