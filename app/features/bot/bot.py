from aiogram import executor, types, Bot, Dispatcher
import logging
from random import choice

from app.config import ARTICLES_BY_NAME
from app.features.users.users_repo import UserRepo, UserScheme


class NewsBot:
    def __init__(self, bot_token: str, user_repo: UserRepo):
        bot = Bot(token=bot_token)
        logging.basicConfig(level=logging.INFO)
        self.dp = Dispatcher(bot)
        self.users = user_repo

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
            username, team = message.chat['username'], ' '.join(message.text.split()[1:])
        except IndexError:
            await message.answer(f'Неверный формат. Попробуйте\n/set <название_команды>')
            return
        if len(self.users.find_all(chat_id=message.chat.id)) == 0:
            await self.users.create(UserScheme(chat_id=message.chat.id, username=username, subscribed_team=team))
        else:
            self.users.put(UserScheme(chat_id=message.chat.id, username=username, subscribed_team=team))

        await message.answer(f'Пользователю {username} успешно '
                             f'была присвоена команда {team}.')

    async def get_team(self, message: types.Message):
        current_user = self.users.get_by_id(str(message.chat.id))
        if current_user is not None:
            await message.answer(f'Для пользователя {current_user.username} '
                                 f'зарегистрирована команда {current_user.subscribed_team}')
        else:
            await message.answer(f'Для пользователя {message.chat["username"]} не '
                                 f'зарегистрирована команда. Это можно сделать '
                                 f'с помощью команды /set <название_команды>')

    async def send_news(self, message: types.Message):
        current_user = self.users.get_by_id(str(message.chat.id))
        if current_user is not None:
            team = current_user.subscribed_team
        else:
            await message.answer(f'Для пользователя {message.chat["username"]} не '
                                 f'зарегистрирована команда. Это можно сделать '
                                 f'с помощью команды /set <название_команды>')
            return
        if team not in ARTICLES_BY_NAME.keys():
            await message.answer('Неизвестная футбольная команда')
            return
        if len(ARTICLES_BY_NAME[team]) == 0:
            await message.answer(f'Пока что новостей по команде {team} нет, но скоро они появятся.')
            return
        title, href = choice(ARTICLES_BY_NAME[team])
        await message.answer(f'[{title}]({href})', parse_mode='Markdown')
