import aioschedule as schedule
from typing import Tuple
import time

from app.features.bot.bot import NewsBot


class BotService:
    def __init__(self, bot: NewsBot):
        self.bot = bot

    async def start_schedule(self):
        while True:
            await self.send_all()
            time.sleep(10)


    async def send_all(self, team: str = None, article: Tuple[str, str] = None):
        team = 'Барселона'
        article = ('abc', 'def')
        users_to_send = self.bot.users.find_all(subscribed_team=team)
        for user in users_to_send:
            await self.bot.bot.send_message(user.chat_id, f'[{article[0]}]({article[1]})', parse_mode='Markdown')
