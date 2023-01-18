import math
import weakref
from typing import Any, Union, List, Dict
from aiogram import Dispatcher
from aiogram.utils.callback_data import CallbackData
from uuid import uuid4
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from app.features.bot.interactive_message_base import InteractiveMessage

_page_select_callback = CallbackData("pwm_page_s", "pvm_id", "page_id")
_unchecked_callback = CallbackData("dont_check_this")


class PagedViewMessage(InteractiveMessage):
    """Сообщение со страничным просмотром
    Необходим вызов PagedViewMessage.init_handlers"""

    _message_by_id: Dict[str, Any] = weakref.WeakValueDictionary()

    @staticmethod
    def get_by_id(ms_id: Union[int, str]):
        return PagedViewMessage._message_by_id[str(ms_id)]

    @staticmethod
    def init_handlers(dp: Dispatcher):
        dp.register_callback_query_handler(handle_page_selection, _page_select_callback.filter())
        dp.register_callback_query_handler(handle_unchecked_callback, _unchecked_callback.filter())

    def __init__(self,
                 records: List[str],
                 records_on_page=7):
        self.id = str(uuid4())
        self.records_on_page = records_on_page
        self.records = records
        self.current_page = 0
        self.records_count = len(records)
        self.page_count = math.ceil(self.records_count / self.records_on_page)
        PagedViewMessage._message_by_id[self.id] = self

    def get_current_page_text(self):
        start_ind = self.current_page * self.records_on_page
        end_ind = (self.current_page + 1) * self.records_on_page
        return "\n\n".join(self.records[start_ind:end_ind])

    def get_markup(self) -> InlineKeyboardMarkup:
        keyboard = [[]]
        if self.page_count > 1:
            next_page = (self.current_page + 1) % self.page_count
            prev_page = (self.current_page - 1) % self.page_count
            buttons = []
            if self.current_page != 0:
                prev_button = InlineKeyboardButton(text="Назад", callback_data=_page_select_callback.new(pvm_id=self.id, page_id=str(prev_page)))
            else:
                prev_button = InlineKeyboardButton(text=" ", callback_data=_unchecked_callback.new())
            buttons.append(prev_button)

            page_num_button = InlineKeyboardButton(text=f"{self.current_page + 1}/{self.page_count}", callback_data=_unchecked_callback.new())
            buttons.append(page_num_button)

            if next_page != 0:
                next_button = InlineKeyboardButton(text="Далее", callback_data=_page_select_callback.new(pvm_id=self.id, page_id=str(next_page)))
            else:
                next_button = InlineKeyboardButton(text=" ", callback_data=_unchecked_callback.new())
            buttons.append(next_button)

            keyboard.append(buttons)
        return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def handle_page_selection(call: CallbackQuery):
    callback = _page_select_callback.parse(call.data)
    try:
        ms = PagedViewMessage.get_by_id(callback["pvm_id"])
    except:
        await call.message.delete()
        return
    ms.current_page = int(callback["page_id"])
    await call.message.edit_text(text=ms.get_current_page_text(), reply_markup=ms.get_markup(), parse_mode='Markdown')


async def handle_unchecked_callback(call: CallbackQuery):
    await call.answer()
