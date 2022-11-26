from abc import ABC, abstractmethod

from typing import List


class BaseRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> object:
        """
        :param id entity identificator
        :return: entity from DB by its id
        """
        pass

    @abstractmethod
    def get_all(self) -> List[object]:
        """
        :return: all entities
        """
        pass

    @abstractmethod
    def create(self, *args, **kwargs) -> object:
        """
        :param kwargs: entity fields
        :return:
        created object
        """
        pass

    @abstractmethod
    def put(self, *args, **kwargs) -> object:
        """
        :param args: entity fields
        :param kwargs: entity fields
        :return: editted object
        """
        pass
