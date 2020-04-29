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
        chapters = [
            Chapter(chapter, pages=[
                Page(page, self._get_page_url(title, chapter, page)) for page in self._get_pages(title, chapter)
             ]) for chapter in self._get_chapters(title)
        ]
        return Manga(title, chapters)

    @abstractmethod
    def crawl(self):
        pass

    @abstractmethod
    def _get_page_url(self, title, chapter, page):
        pass

    @abstractmethod
    def _get_pages(self, title, chapter):
        pass

    @abstractmethod
    def _get_chapters(self, title):
        pass