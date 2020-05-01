from abc import ABC, abstractmethod

from ..manga import Manga, Chapter, Page


class Source(ABC):

    BASE_URL = ''
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def get_manga(self, title):
        return Manga(title, self.get_chapters(title))

    @abstractmethod
    def crawl(self):
        pass

    @abstractmethod
    def get_chapters(self, title):
        pass

    @abstractmethod
    def get_pages(self, title, chapter):
        pass
