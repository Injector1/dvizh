from aiogram.types import CallbackQuery
from multiselect_keyboard import InlineMultiselect, \
    multiset_item_select_callback, multiset_accept_changes_callback, multiset_page_select_callback, \
    multiset_finish_selection_callback, unchecked_callback


# TODO фиксануть
from USING_EXAMPLE import dp
# dp = STASH_using_example.dp # TODO объявлять диспачер при подключении пакета, как это сделать хз))


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
