import threading
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..manga import Manga, Chapter, Page


class DocumentParser(ABC):

    def __init__(self, context):
        self.context = context

    def parse(self, title):
        self.context.url = self._get_url(title)
        self.context.page_content = self._get_page_content(title)
        return {
            "title": self._parse_title(),
            "author": self._parse_author(),
            "artist": self._parse_artist(),
            "description": self._parse_description(),
            "tags": self._parse_tags(),
            "completed": self._parse_completion_status(),
            "url": self.context.url
        }

    @abstractmethod
    def _get_page_content(self, title):
        pass

    @abstractmethod
    def _get_url(self, title):
        pass

    @abstractmethod
    def _parse_title(self):
        pass

    @abstractmethod
    def _parse_author(self):
        pass

    @abstractmethod
    def _parse_artist(self):
        pass

    @abstractmethod
    def _parse_description(self):
        pass

    @abstractmethod
    def _parse_tags(self):
        pass

    @abstractmethod
    def _parse_completion_status(self):
        pass


class Source(ABC):

    BASE_URL = ''
    CRAWLER_MAX_WORKERS = 100
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
        manga_list = self.get_manga_list()
        return [document for document in self.generate_indexable_documents(manga_list)]

    @abstractmethod
    def get_manga_list(self):
        pass

    @abstractmethod
    def _get_document_parser(self, context) -> DocumentParser:
        pass

    def generate_indexable_documents(self, titles):
        thread_context = threading.local()
        parser = self._get_document_parser(thread_context)
        with ThreadPoolExecutor(max_workers=self.CRAWLER_MAX_WORKERS) as executor:
            futures = [executor.submit(parser.parse, title) for title in titles]
            for future in as_completed(futures):
                try:
                    yield future.result()
                except Exception:
                    pass
