import logging
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils import executor
from AMOGUS import AMOGUS

token = '5914366318:AAFihB-KhrA_8-AMX4XuRhwmwHkXgzYEDug'
bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
DATABASE = dict()

# НАЧАЛО ПРИМЕРА


@dp.message_handler(Command("start"))
async def amogus1(message: Message):
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
    print(f"Пользвователь с id: {user_id} выбрал команды: {teams_ids}")


async def send_amogus(chat_id: int):
    await bot.send_message(chat_id=chat_id, text=AMOGUS)


# КОНЕЦ ПРИМЕРА


# TODO сделать чтобы operation_with_selected и on_finish_selection могли быть и не асинхронными
#  (вызываются они в handle_accept_changes и handle_finish_selection)
# TODO ВСЁ ЧТО НИЖЕ ПЕРЕНЕСЬТИ В multiselect_keyboard_handler



from aiogram.types import CallbackQuery
from multiselect_keyboard import InlineMultiselect, \
    multiset_item_select_callback, multiset_accept_changes_callback, multiset_page_select_callback, \
    multiset_finish_selection_callback, unchecked_callback


@dp.callback_query_handler(multiset_item_select_callback.filter())
async def handle_item_selection(call: CallbackQuery):
    callback = multiset_item_select_callback.parse(call.data)
    ms = InlineMultiselect.keyboard_by_id[callback["ms_id"]]
    item_id = callback["item_id"]
    ms.select_item(int(item_id))
    await call.message.edit_reply_markup(reply_markup=ms.get_markup())


@dp.callback_query_handler(multiset_page_select_callback.filter())
async def handle_page_selection(call: CallbackQuery):
    callback = multiset_page_select_callback.parse(call.data)
    ms = InlineMultiselect.keyboard_by_id[callback["ms_id"]]
    ms.current_page = int(callback["page_id"])
    await call.message.edit_reply_markup(reply_markup=ms.get_markup())


@dp.callback_query_handler(unchecked_callback.filter())
async def handle_unchecked_callback(call: CallbackQuery):
    await call.answer()


@dp.callback_query_handler(multiset_accept_changes_callback.filter())
async def handle_accept_changes(call: CallbackQuery):
    callback = multiset_accept_changes_callback.parse(call.data)
    ms = InlineMultiselect.keyboard_by_id[callback["ms_id"]]
    selected_item_ids = [x for x in ms.items if x in ms.selected_items]
    await ms.operation_with_selected(selected_item_ids)
    await ms.on_finish_selection()
    del ms
    await call.message.delete()


@dp.callback_query_handler(multiset_finish_selection_callback.filter())
async def handle_finish_selection(call: CallbackQuery):
    callback = multiset_finish_selection_callback.parse(call.data)
    ms = InlineMultiselect.keyboard_by_id[callback["ms_id"]]
    await ms.on_finish_selection()
    del ms
    await call.message.delete()


executor.start_polling(dp, skip_updates=True)
