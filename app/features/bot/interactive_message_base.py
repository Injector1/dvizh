from abc import ABC, abstractmethod
from typing import Union


class InteractiveMessage(ABC):
    @staticmethod
    @abstractmethod
    def init_handlers(self):
        """
        init handlers for this keyboard
        """

    @abstractmethod
    def get_markup(self):
        """
        :return: InlineKeyboardMarkup
        """