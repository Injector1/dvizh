import asyncio
from aiogram import Bot
from app.features.bot.bot import NewsBot


class BotService:
    def __init__(self, bot: NewsBot):
        self.bot = bot

    async def send_all(self, team: str, article: tuple[str, str]):
        users_to_send = self.bot.users.find_all(subscribed_team=team)
        b = Bot(token='5914366318:AAFihB-KhrA_8-AMX4XuRhwmwHkXgzYEDug')
        for user in users_to_send:
            await b.send_message(user.chat_id, f'[{article[0]}]({article[1]})', parse_mode='Markdown')
