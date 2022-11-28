import logging
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils import executor
from AMOGUS import AMOGUS
from custom_inline_keyboards.select_keyboard.select_keyboard import InlineSelect
from multiselect_keyboard.multiselect_keyboard import InlineMultiselect

token = '5907318542:AAGEJ5Fkw8Jx0KipolIbGvdDaPZSfD44HTI'
bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
DATABASE = dict()

InlineMultiselect.init_handlers(dp)
InlineSelect.init_handlers(dp)


@dp.message_handler(Command("s"))
async def select_example(message: Message):
    items = ["Sugoma", "Amogus", "Sus", "Niggers", "Figgers", "Nill", "Kiggers"]
    items_ids = [0, 1, 2, 3, 4, 5, 6]
    already_selected = DATABASE.get(message.from_user.id)
    if already_selected is None:
        already_selected = []
    ms = InlineSelect(item_ids=items_ids,
                      get_item_name_by_id=lambda id: items[id],
                      operation_with_selected=lambda ids: add_teams_to_user(message.from_user.id, ids),
                      on_finish_selection=lambda: send_amogus(message.chat.id),
                      selection_mark="ඞ ", max_rows=2, columns=2,
                      selected_item=already_selected)
    await message.answer(text="Выберите своего бойца:", reply_markup=ms.get_markup())


@dp.message_handler(Command("ms"))
async def multiselect_example(message: Message):
    items = ["Sugoma", "Amogus", "Sus", "Niggers", "Figgers", "Nill", "Kiggers"]
    items_ids = [0, 1, 2, 3, 4, 5, 6]
    already_selected = DATABASE.get(message.from_user.id)
    if already_selected is None:
        already_selected = []
    ms = InlineMultiselect(item_ids=items_ids,
                           get_item_name_by_id=lambda id: items[id],
                           operation_with_selected=lambda ids: add_teams_to_user(message.from_user.id, ids),
                           on_finish_selection=lambda: send_amogus(message.chat.id),
                           selection_mark="ඞ ", max_rows=2, columns=2,
                           selected_item=already_selected)
    await message.answer(text="Выберите своего бойца:", reply_markup=ms.get_markup())


async def add_teams_to_user(user_id: int, teams_ids: list[int]):
    DATABASE[user_id] = teams_ids
    print(f"Пользователь с id: {user_id} выбрал команды: {teams_ids}")


async def send_amogus(chat_id: int):
    await bot.send_message(chat_id=chat_id, text=AMOGUS)


executor.start_polling(dp, skip_updates=True)
