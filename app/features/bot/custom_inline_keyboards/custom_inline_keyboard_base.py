from abc import ABC, abstractmethod
from typing import Union
from app.features.bot.interactive_message_base import InteractiveMessage


class CustomInlineKeyboard(InteractiveMessage, ABC):
    @staticmethod
    @abstractmethod
    def get_by_id(ms_id: Union[int, str]):
        """
        :return: CustomInlineKeyboard
        """