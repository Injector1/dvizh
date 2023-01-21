import datetime

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import executor, types, Bot, Dispatcher
import logging
from random import choice

from aiogram.utils.callback_data import CallbackData

from app.config import ARTICLES_BY_NAME
from app.features.bot.interactive_message_base import InteractiveMessage
from app.features.bot.paged_view.paged_view import PagedViewMessage
from app.features.users.repository import UserRepository, UserScheme
from app.features.telegraf.json_repo import JsonRepository
from app.features.bot.custom_inline_keyboards import InlineSelect


DP: Dispatcher
_subc_callback = CallbackData("subc", "flag")


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
        global DP
        DP = dp
        self.dp = dp
        self.users = user_repository
        self.articles = article_repository
        self.last_interactive_msg_by_chat_id: dict[str, InteractiveMessage] = dict()
        InlineSelect.init_handlers(self.dp)
        PagedViewMessage.init_handlers(self.dp)

        button_news = KeyboardButton('Новости')
        button_menu = KeyboardButton('Меню')
        button_subc = KeyboardButton('Подписка')

        dp.register_message_handler(self.show_menu, lambda m: m.text == "Меню")
        dp.register_message_handler(self.send_news, lambda m: m.text == "Новости")
        dp.register_message_handler(self.subscribe, lambda m: m.text == "Подписка")
        dp.register_callback_query_handler(self.handle_subscribe_callback, _subc_callback.filter())

        self.keyboard = ReplyKeyboardMarkup(keyboard=[[button_news, button_menu, button_subc]],
                                            resize_keyboard=True)

    def add_commands(self) -> None:
        commands = [
            (self.review, ['r']),
            (self.on_start, ['start']),
            (self.show_menu, ['menu']),
            (self.get_team, ['get', 'help']),
            (self.send_news, ['news'])
        ]
        for command in commands:
            self.dp.register_message_handler(command[0], commands=command[1])
        executor.start_polling(self.dp, skip_updates=True)

    async def review(self, message: types.Message):
        await message.answer(f'🔥Вышло новое видео: "Реал - Барселона. Обзор финального матча Суперкубка Испании 15.01.2023⚽️\n\n'
                             f'https://www.youtube.com/watch?v=hqfvT5YKxps"', reply_markup=self.keyboard)

    async def on_start(self, message: types.Message):
        await message.answer(f'Данный бот позволяет отслеживать новости о вашей любимой футбольной команде.\n'
                             f'Он будет уведомлять вас при появлении свежих новостей.   ', reply_markup=self.keyboard)

    async def add_team(self, message: types.Message, team: str):
        current_user = self.users.get_by_id(str(message.from_user.id))
        user = UserScheme(
            chat_id=str(message.from_user.id),
            username=message.from_user.username or message.from_user.id,
            subscribed_team=team
        )
        if len(self.users.find_all(chat_id=str(message.from_user.id))) == 0:
            self.users.create(user)
        else:
            self.users.put(user)

    async def subscribe(self, message: types.Message):
        await self.get_team(message)

    async def handle_subscribe_callback(self, call: CallbackQuery):
        callback = _subc_callback.parse(call.data)
        sub_flag = callback["flag"]  #"sub" or "unsub"
        if sub_flag == "sub":
            await call.message.edit_text(text="✅ Вы подписались на уведомления о новостях", reply_markup=None)
        else:
            await call.message.edit_text(text="❌ Вы отписались от уведомлений", reply_markup=None)

    async def get_team(self, message: types.Message):
        current_user = self.users.get_by_id(str(message.from_user.id))
        if current_user is not None:

            inline_btn_1 = InlineKeyboardButton('❌', callback_data=_subc_callback.new(flag="unsub"))
            inline_btn_2 = InlineKeyboardButton('✅', callback_data=_subc_callback.new(flag="sub"))
            inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[inline_btn_2, inline_btn_1]])

            await message.answer(f'Желаете подписаться на уведомления о новостях команды {current_user.subscribed_team}?', reply_markup=inline_keyboard)
        else:
            await message.answer(f'Ой! Вы не выбрали какую команду отслеживать! '
                                 f'Это можно сделать через меню.', reply_markup=self.keyboard)

    async def send_news(self, message: types.Message):
        current_user = self.users.get_by_id(str(message.from_user.id))
        if current_user is not None:
            team = current_user.subscribed_team
        else:
            await message.answer(f'Ой! Вы не выбрали какую команду отслеживать! '
                                 f'Это можно сделать через меню.', reply_markup=self.keyboard)
            return
        m = self.articles.find_all(team_name=team)
        if len(m) == 0:
            await message.answer(f'Пока что новостей по команде {team} нет, но скоро они появятся.', reply_markup=self.keyboard)
            return
        response = []
        dates = []
        months = {'01':'января', '02': 'февраля', '03':'марта', '04':'апреля', '05':'мая', '06':'июня',
                  '07':'июля', '08':'августа', '09':'сентября', '10':'октября', '11':'ноября', '12':'декабря'}
        for k in range(min(len(m), 10)):
            i = len(m) - k - 1
            m_date = m[i].date
            if m_date not in dates:
                dates.append(m_date)
                day = m_date.split('-')[2]
                month = months[m_date.split('-')[1]]
                response.append(f'\n🕑 {day} {month}\n\n')
            else:
                response.append('')
            title, href = m[i].title, m[i].url
            response[-1] += f' ⚡️ [{title}]({href})'
        pw = PagedViewMessage(response, records_on_page=5)
        self.last_interactive_msg_by_chat_id[message.chat.id] = pw
        await message.answer(text=pw.get_current_page_text(), reply_markup=pw.get_markup(), parse_mode='Markdown')

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
        self.last_interactive_msg_by_chat_id[message.chat.id] = ms
        await message.answer(text="Выберите команду из списка", reply_markup=ms.get_markup())
