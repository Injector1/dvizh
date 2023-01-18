import logging
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils import executor

from app.features.bot.paged_view.paged_view import PagedViewMessage

token = '5907318542:AAGEJ5Fkw8Jx0KipolIbGvdDaPZSfD44HTI'
bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
DATABASE = dict()
PagedViewMessage.init_handlers(dp)

CURRENT_REPLY = None

@dp.message_handler(Command("start"))
async def amogus1(message: Message):
    items = ["Sugoma", "Amogus", "Sus", "Niggers", "Figgers", "Nill", "Kiggers", "Негры", "Чурки", "Сасибака"]
    ms = PagedViewMessage(items, records_on_page=4)
    global CURRENT_REPLY
    CURRENT_REPLY = ms
    await message.answer(text=ms.get_current_page_text(), reply_markup=ms.get_markup())


executor.start_polling(dp, skip_updates=True)