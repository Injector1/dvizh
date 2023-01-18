import datetime

from aiogram import executor, types, Bot, Dispatcher
import logging
from random import choice

from app.config import ARTICLES_BY_NAME
from app.features.users.repository import UserRepository, UserScheme
from app.features.telegraf.json_repo import JsonRepository
from app.features.bot.custom_inline_keyboards import InlineSelect


class NewsBot:
    def __init__(
            self,
            bot: Bot,
            dp: Dispatcher,
            user_repository: UserRepository,
            article_repository: JsonRepository,
    ):
        self.bot = bot
        logging.basicConfig(level=logging.INFO)
        self.dp = dp
        self.users = user_repository
        self.articles = article_repository
        InlineSelect.init_handlers(self.dp)

    def add_commands(self) -> None:
        commands = [
            (self.on_start, ['start']),
            (self.show_menu, ['menu']),
            (self.get_team, ['get', 'help']),
            (self.send_news, ['news'])
        ]
        for command in commands:
            self.dp.register_message_handler(command[0], commands=command[1])
        executor.start_polling(self.dp, skip_updates=True)

    async def on_start(self, message: types.Message):
        await message.answer(f'Данный бот позволяет отслеживать новости о вашей любимой футбольной команде.\n'
                             f'Он будет уведомлять вас при появлении свежих новостей.\n\n'
                             f'/menu - выбор команды')

    async def add_team(self, message: types.Message, team: str):
        user = UserScheme(
            chat_id=str(message.from_user.id),
            username=message.from_user.username,
            subscribed_team=team
        )
        if len(self.users.find_all(chat_id=str(message.from_user.id))) == 0:
            self.users.create(user)
        else:
            self.users.put(user)

    async def get_team(self, message: types.Message):
        current_user = self.users.get_by_id(str(message.from_user.id))
        if current_user is not None:
            await message.answer(f'/news - чтобы получить новости по команде {current_user.subscribed_team}')
        else:
            await message.answer(f'Для пользователя {message.chat["username"]} не '
                                 f'зарегистрирована команда. Это можно сделать '
                                 f'с помощью команды /menu')

    async def send_news(self, message: types.Message):
        current_user = self.users.get_by_id(str(message.from_user.id))
        if current_user is not None:
            team = current_user.subscribed_team
        else:
            await message.answer(f'Для пользователя {message.from_user.username} не '
                                 f'зарегистрирована команда. Это можно сделать '
                                 f'с помощью команды /menu')
            return
        m = self.articles.find_all(team_name=team)
        if len(m) == 0:
            await message.answer(f'Пока что новостей по команде {team} нет, но скоро они появятся.')
            return
        response = ''
        dates = []
        months = {'01':'января', '02': 'февраля', '03':'марта', '04':'апреля', '05':'мая', '06':'июня',
                  '07':'июля', '08':'августа', '09':'сентября', '10':'октября', '11':'ноября', '12':'декабря'}
        for i in range(min(len(m), 10)):
            m_date = m[i].date
            if m_date not in dates:
                dates.append(m_date)
                day = m_date.split('-')[2]
                month = months[m_date.split('-')[1]]
                response += f'\n🕑 {day} {month}\n'
            title, href = m[i].title, m[i].url
            response += f' ⚡️ [{title}]({href})\n\n'
        await message.answer(response, parse_mode='Markdown')

    async def show_menu(self, message: types.Message):
        items = list(ARTICLES_BY_NAME.keys())
        items_ids = list(range(len(ARTICLES_BY_NAME.keys())))
        current_user = self.users.get_by_id(str(message.from_user.id))
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
