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
    def get_chapters(self, title):
        pass

    @abstractmethod
    def get_pages(self, title, chapter):
        pass

    def crawl(self):
        manga_list = self._get_manga_list()
        titles = self._parse_manga_list(manga_list)
        return self._get_indexable_documents_from_source(titles)

    @abstractmethod
    def _get_manga_list(self):
        pass


    @abstractmethod
    def _parse_manga_list(self, page_content):
        pass

    @abstractmethod
    def _get_indexable_documents_from_source(self, titles):
        pass
