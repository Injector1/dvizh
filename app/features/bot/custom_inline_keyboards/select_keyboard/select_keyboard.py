import math
from typing import Callable, Any, Union, Dict, List

from aiogram import Dispatcher
from aiogram.utils.callback_data import CallbackData
from uuid import uuid4
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.features.bot.custom_inline_keyboards.custom_inline_keyboard import CustomInlineKeyboard


_item_select_callback = CallbackData("s_select_item", "ms_id", "item_id")
_page_select_callback = CallbackData("s_select_page", "ms_id", "page_id")
_accept_changes_callback = CallbackData("s_accept", "ms_id")
_finish_selection_callback = CallbackData("s_finish", "ms_id")
_unchecked_callback = CallbackData("dont_check_this")

CANCEL_BUTTON_TEXT = "Отмена"
ACCEPT_BUTTON_TEXT = "Сохранить"


class InlineSelect(CustomInlineKeyboard):
    """Список с выбором
    Необходим вызов InlineSelect.init_handlers"""

    _keyboard_by_id: Dict[str, Any] = dict()

    @staticmethod
    def get_by_id(ms_id: Union[int, str]):
        return InlineSelect._keyboard_by_id[str(ms_id)]

    @staticmethod
    def init_handlers(dp: Dispatcher):
        dp.register_callback_query_handler(handle_item_selection, _item_select_callback.filter())
        dp.register_callback_query_handler(handle_page_selection, _page_select_callback.filter())
        dp.register_callback_query_handler(handle_unchecked_callback, _unchecked_callback.filter())
        dp.register_callback_query_handler(handle_accept_changes, _accept_changes_callback.filter())
        dp.register_callback_query_handler(handle_finish_selection, _finish_selection_callback.filter())

    def __init__(self,
                 item_ids: List[int],
                 get_item_name_by_id: Callable[[int], str],
                 operation_with_selected: Callable[[List[int]], Any],
                 on_finish_selection: Callable[[], Any],
                 selected_item=None,
                 selection_mark="✓ ", columns=1, max_rows=7):
        """
        get_item_name_by_id:
                функция получения отображаемого имени предмета по его id

        operation_with_selected:
                функция-обработчик списка выбранных id предметов после нажатия кнопки "Сохранить"

        on_finish_selection:
                функция, вызываемая после нажатия кнопки "Сохранить" или "Отмена", выполняемая после operation_with_selected

        selected_item:
                список заранее выбранных предметов

        selection_mark:
                отметка выбранных предметов
        """
        if selected_item is None:
            selected_item = []
        self.id = str(uuid4())
        self.items = item_ids
        self.selected_items = set(selected_item)
        self.get_item_name_by_id = get_item_name_by_id
        self.operation_with_selected = operation_with_selected
        self.on_finish_selection = on_finish_selection

        self.selection_mark = selection_mark
        self.columns = columns
        self.max_rows = max_rows
        self.current_page = 0
        self.page_count = math.ceil(len(self.items) / (self.max_rows * self.columns))
        InlineSelect._keyboard_by_id[self.id] = self

    def select_item(self, item_id: int):
        if item_id in self.selected_items:
            self.selected_items.remove(item_id)
        else:
            self.selected_items.clear()
            self.selected_items.add(item_id)

    def get_markup(self) -> InlineKeyboardMarkup:
        keyboard = [[]]
        start_index = self.current_page * (self.max_rows * self.columns)
        end_index = min(start_index + (self.max_rows * self.columns), len(self.items))
        for item in self.items[start_index:end_index]:
            display_name = self.get_item_name_by_id(item)
            if item in self.selected_items:
                display_name = self.selection_mark + display_name
            button = InlineKeyboardButton(text=display_name,
                                          callback_data=_item_select_callback.new(ms_id=self.id,
                                                                                          item_id=str(item)))
            if len(keyboard[-1]) >= self.columns:
                keyboard.append([])
            keyboard[-1].append(button)

        if self.page_count > 1:
            next_page = (self.current_page + 1) % self.page_count
            prev_page = (self.current_page - 1) % self.page_count
            prev_button = InlineKeyboardButton(text="<",
                                               callback_data=_page_select_callback.new(ms_id=self.id,
                                                                                       page_id=str(prev_page)))
            next_button = InlineKeyboardButton(text=">",
                                               callback_data=_page_select_callback.new(ms_id=self.id,
                                                                                       page_id=str(next_page)))
            page_num_button = InlineKeyboardButton(text=f"{self.current_page + 1}/{self.page_count}",
                                                   callback_data=_unchecked_callback.new())
            keyboard.append([prev_button, page_num_button, next_button])

        accept_button = InlineKeyboardButton(text=ACCEPT_BUTTON_TEXT,
                                             callback_data=_accept_changes_callback.new(ms_id=self.id))
        undo_button = InlineKeyboardButton(text=CANCEL_BUTTON_TEXT,
                                           callback_data=_finish_selection_callback.new(ms_id=self.id))
        keyboard.append([undo_button, accept_button])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def __del__(self):
        InlineSelect._keyboard_by_id.pop(self.id)


async def handle_item_selection(call: CallbackQuery):
    callback = _item_select_callback.parse(call.data)
    ms = InlineSelect._keyboard_by_id[callback["ms_id"]]
    item_id = callback["item_id"]
    ms.select_item(int(item_id))
    await call.message.edit_reply_markup(reply_markup=ms.get_markup())


async def handle_page_selection(call: CallbackQuery):
    callback = _page_select_callback.parse(call.data)
    ms = InlineSelect._keyboard_by_id[callback["ms_id"]]
    ms.current_page = int(callback["page_id"])
    await call.message.edit_reply_markup(reply_markup=ms.get_markup())


async def handle_unchecked_callback(call: CallbackQuery):
    await call.answer()


async def handle_accept_changes(call: CallbackQuery):
    callback = _accept_changes_callback.parse(call.data)
    ms = InlineSelect._keyboard_by_id[callback["ms_id"]]
    selected_item_ids = [x for x in ms.items if x in ms.selected_items]
    await ms.operation_with_selected(selected_item_ids)
    await ms.on_finish_selection()
    del ms
    await call.message.delete()


async def handle_finish_selection(call: CallbackQuery):
    callback = _finish_selection_callback.parse(call.data)
    ms = InlineSelect._keyboard_by_id[callback["ms_id"]]
    await ms.on_finish_selection()
    del ms
    await call.message.delete()
