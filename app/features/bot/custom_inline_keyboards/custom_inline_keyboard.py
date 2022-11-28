from abc import ABC, abstractmethod
from typing import Union


class CustomInlineKeyboard(ABC):
    @staticmethod
    @abstractmethod
    def init_handlers(self):
        """
        init handlers for this keyboard
        """

    @staticmethod
    @abstractmethod
    def get_by_id(ms_id: Union[int, str]):
        """
        :return: CustomInlineKeyboard
        """
