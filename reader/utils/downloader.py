import os
import re

import requests

from .common import ROOT_DIRECTORY
from ..manga import Manga, Chapter, Page

DEFAULT_DOWNLOAD_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'manga')
MANGA_DOWNLOAD_DIRECTORY = os.getenv('MANGA_HOME', DEFAULT_DOWNLOAD_DIRECTORY)


class Downloader(object):

    def __init__(self, manga_home=MANGA_DOWNLOAD_DIRECTORY):
        self.manga_home = manga_home

    def download_manga(self, manga: Manga, force=False):
        for chapter in manga.chapters:
            self.download_chapter(manga.title, chapter, force=force)

    def download_chapter(self, title, chapter: Chapter, force=False):
        title = self.normalize(title)
        dirpath = os.path.join(self.manga_home, title)
        self._ChapterDownloader(dirpath, chapter).download(force)

    @staticmethod
    def normalize(input_str):
        output = re.sub('[^A-Za-z0-9 ]+', '', input_str)
        return output.replace(' ', '-').lower()

    class _ChapterDownloader(object):

        def __init__(self, path, chapter):
            self.chapter = chapter
            self.chapter_dir = os.path.join(path, str(chapter.number))

        def download(self, force=False):
            if os.path.exists(self.chapter_dir) and not force:
                return ()  # chapter exists on disk, skip
            os.makedirs(self.chapter_dir, exist_ok=True)
            for page in self.chapter.pages:
                self._download_page(page)

        def _download_page(self, page: Page):
            filepath = self._build_page_filepath(page)
            self._stream_remote_image(page.image_url, filepath)

        def _build_page_filepath(self, page):
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
