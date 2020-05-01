import os

import requests

from .common import ROOT_DIRECTORY
from ..manga import Manga, Chapter, Page

DEFAULT_DOWNLOAD_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'manga')
MANGA_DOWNLOAD_DIRECTORY = os.getenv('MANGA_HOME', DEFAULT_DOWNLOAD_DIRECTORY)


class Downloader(object):

    def __init__(self, manga_home=MANGA_DOWNLOAD_DIRECTORY):
        self.manga_home = manga_home
        self.chapter_dir = None

    def download_manga(self, manga: Manga):
        for chapter in manga.chapters:
            self._build_chapter_dirpath(manga, chapter)
            if not os.path.exists(self.chapter_dir):
                self.download_chapter(manga, chapter)

    def _build_chapter_dirpath(self, manga, chapter):
        self.chapter_dir = os.path.join(self.manga_home, manga.title, str(chapter.number))

    def download_chapter(self, manga: Manga, chapter: Chapter):
        if not self.chapter_dir:
            self._build_chapter_dirpath(manga, chapter)
        os.makedirs(self.chapter_dir, exist_ok=True)
        for page in chapter.pages:
            self._download_page(page)

    def _download_page(self, page: Page):
        filepath = self._build_page_filepath(page)
        self._stream_remote_image(page.image_url, filepath)

    def _build_page_filepath(self, page):
        if not self.chapter_dir:
            raise Exception("No ")
        filetype = page.image_url.split('.')[-1]
        filename = f'{page.number}.{filetype}'
        return os.path.join(self.chapter_dir, filename)

    def _stream_remote_image(self, url, filepath):
        stream = requests.get(url, stream=True)
        stream.raise_for_status()
        self._stream_image_to_file(stream, filepath)

    def _stream_image_to_file(self, stream, filepath):
        with open(filepath, 'wb') as image_file:
            for chunk in stream.iter_content(1024):
                image_file.write(chunk)
