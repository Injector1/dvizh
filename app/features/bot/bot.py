from aiogram import executor, types, Bot, Dispatcher
import logging
from random import choice

from app.config import ARTICLES_BY_NAME
from app.features.users.users_repo import UserRepo, UserScheme
from app.features.bot.custom_inline_keyboards import InlineSelect


class NewsBot:
    def __init__(self, bot_token: str, user_repo: UserRepo):
        bot = Bot(token=bot_token)
        logging.basicConfig(level=logging.INFO)
        self.dp = Dispatcher(bot)
        self.users = user_repo
        InlineSelect.init_handlers(self.dp)

    def add_commands(self) -> None:
        commands = [
            (self.on_start, ['start']),
            (self.show_menu, ['menu']),
            (self.get_team, ['get']),
            (self.send_news, ['news'])
        ]
        for command in commands:
            self.dp.register_message_handler(command[0], commands=command[1])
        executor.start_polling(self.dp, skip_updates=True)

    async def on_start(self, message: types.Message):
        await message.answer(f'/menu - выбор команды\n'
                             f'/news - получить 1 из последних новостей')

    async def add_team(self, message: types.Message, team: str):
        username = message.chat['username']
        if len(self.users.find_all(chat_id=str(message.chat.id))) == 0:
            await self.users.create(UserScheme(chat_id=str(message.chat.id), username=username, subscribed_team=team))
        else:
            self.users.put(UserScheme(chat_id=str(message.chat.id), username=username, subscribed_team=team))

    async def get_team(self, message: types.Message):
        current_user = self.users.get_by_id(str(message.chat.id))
        if current_user is not None:
            await message.answer(f'Вы теперь отслеживаете команду {current_user.subscribed_team}')
        else:
            await message.answer(f'Для пользователя {message.chat["username"]} не '
                                 f'зарегистрирована команда. Это можно сделать '
                                 f'с помощью команды /menu')

    async def send_news(self, message: types.Message):
        current_user = self.users.get_by_id(str(message.chat.id))
        if current_user is not None:
            team = current_user.subscribed_team
        else:
            await message.answer(f'Для пользователя {message.chat["username"]} не '
                                 f'зарегистрирована команда. Это можно сделать '
                                 f'с помощью команды /menu')
            return
        if len(ARTICLES_BY_NAME[team]) == 0:
            await message.answer(f'Пока что новостей по команде {team} нет, но скоро они появятся.')
            return
        response = ''  # f'[{title}]({href})'
        for i in range(min(len(ARTICLES_BY_NAME[team]), 10)):
            title, href = ARTICLES_BY_NAME[team][i]
            response += f'[{title}]({href})\n'
        await message.answer(response, parse_mode='Markdown')

    async def show_menu(self, message: types.Message):
        items = list(ARTICLES_BY_NAME.keys())
        items_ids = list(range(len(ARTICLES_BY_NAME.keys())))
        current_user = self.users.get_by_id(str(message.chat.id))
        if current_user is None:
            already_selected = []
        else:
            already_selected = [current_user.subscribed_team]
        ms = InlineSelect(item_ids=items_ids,
                          get_item_name_by_id=lambda id: items[id],
                          operation_with_selected=lambda ids: self.add_team(message, items[ids[0]]),
                          on_finish_selection=lambda: self.get_team(message),
                          selection_mark="✅", max_rows=6, columns=1,
                          selected_item=already_selected)
        await message.answer(text="Выберите команду из списка", reply_markup=ms.get_markup())
