import re
import threading
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed

from ..manga import Manga, Chapter, Page


class DocumentParser(ABC):

    def __init__(self, context):
        self.context = context

    def parse(self, title):
        self.context.url = self._get_url(title)
        self.context.parser = self._get_page_parser(title)
        return {
            "title": str(self._parse_title()),
            "author": str(self._parse_author()),
            "artist": str(self._parse_artist()),
            "description": str(self._parse_description()),
            "tags": str(self._parse_tags()),
            "completed": bool(self._parse_completion_status()),
            "url": str(self.context.url)
        }

    @abstractmethod
    def _get_page_parser(self, title):
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


class Scraper(ABC):

    def __init__(self, title):
        self.title = title

    @abstractmethod
    def get_chapters(self):
        pass

    def get_pages(self, chapter):
        pages = range(1, self._get_page_count(chapter) + 1)
        return [Page(page, self._get_page_url(chapter, page)) for page in pages]

    @abstractmethod
    def _get_page_count(self, chapter):
        pass

    @abstractmethod
    def _get_page_url(self, chapter, page):
        pass


class Source(ABC):

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    @staticmethod
    def normalize(input_str):
        output = re.sub('[^A-Za-z0-9 ]+', '', input_str)
        return output.replace(' ', '-').lower()

    def get_manga(self, title):
        scraper = self.get_scraper(title)
        chapters = scraper.get_chapters()
        return Manga(title, chapters=[Chapter(chapter, pages=scraper.get_pages(chapter)) for chapter in chapters])

    @abstractmethod
    def get_scraper(self, title) -> Scraper:
        pass

    def crawl(self):
        thread_context = threading.local()
        parser = self.get_document_parser(thread_context)
        documents = []
        for title in self.get_manga_list():
            try:
                documents.append(parser.parse(title))
            except Exception:
                pass
        return documents

    @abstractmethod
    def get_manga_list(self):
        pass

    @abstractmethod
    def get_document_parser(self, context: threading.local) -> DocumentParser:
        pass
