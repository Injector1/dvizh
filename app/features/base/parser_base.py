from abc import ABC, abstractmethod, abstractproperty


class BaseParser(ABC):
    @property
    @abstractmethod
    def base_url(self):
        """
        :return: base url of sports website
        """
        pass

    @abstractmethod
    def parse(self):
        """
        :return:
        Parsed view of article
        """
        pass

    @abstractmethod
    def get_markdown_view(self):
        """
        :return: markdown view of article
        """
        pass

    @abstractmethod
    def get_html_view(self):
        """
        :return: html view of article
        """
        pass

    @abstractmethod
    def get_url_by_tag(self, tag: str) -> str:
        """
        :return: url to source website with tag
        """
        pass