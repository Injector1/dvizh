import logging
from aiogram import Bot, Dispatcher


token = '5914366318:AAFihB-KhrA_8-AMX4XuRhwmwHkXgzYEDug'
bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
