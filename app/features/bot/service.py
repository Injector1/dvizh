from aiogram import Bot
from typing import Tuple

from app.features.bot.bot import NewsBot


class BotService:
    def __init__(self, bot: NewsBot):
        self.bot = bot

    async def send_all(self, team: str, article: Tuple[str, str]):
        users_to_send = self.bot.users.find_all(subscribed_team=team)
        for user in users_to_send:
            await self.bot.send_message(user.chat_id, f'[{article[0]}]({article[1]})', parse_mode='Markdown')
