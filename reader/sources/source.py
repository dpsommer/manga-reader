from abc import ABC, abstractmethod

from ..manga import Manga, Chapter, Page


class DocumentParser(ABC):

    def __init__(self):
        self.page_content = None

    def parse(self, title):
        self.page_content = self._get_page_content(title)
        title = self._parse_title()
        return Manga.document(
            title=title,
            author=self._parse_author(),
            artist=self._parse_artist(),
            description=self._parse_description(),
            tags=self._parse_tags(),
            completed=self._parse_completion_status()
        )

    @abstractmethod
    def _get_page_content(self, title):
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
    def _get_document_parser(self) -> DocumentParser:
        pass

    def _get_indexable_documents_from_source(self, titles):
        parser = self._get_document_parser()
        documents = []
        for title in titles:
            try:
                document = parser.parse(title)
                documents.append(document)
            except Exception as e:
                print(str(e))
        return documents
