import os

import requests

from .common import ROOT_DIRECTORY
from ..sources import MangaReader, Source

DEFAULT_DOWNLOAD_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'manga')
MANGA_DOWNLOAD_DIRECTORY = os.getenv('MANGA_HOME', DEFAULT_DOWNLOAD_DIRECTORY)


class Downloader(object):

    def __init__(self, manga_home=MANGA_DOWNLOAD_DIRECTORY):
        self.manga_home = manga_home

    def download_manga(self, manga):
        for chapter in manga.chapters.keys():
            chapter_dir = self._build_chapter_dirpath(manga, chapter)
            if not os.path.exists(chapter_dir):
                self.download_chapter(manga, chapter, chapter_dir)

    def _build_chapter_dirpath(self, manga, chapter):
        return os.path.join(self.manga_home, manga.title, str(chapter))

    def download_chapter(self, manga, chapter, chapter_dir=None):
        chapter_dir = chapter_dir or self._build_chapter_dirpath(manga, chapter)
        os.makedirs(chapter_dir, exist_ok=True)
        for page, img_url in manga.chapters[chapter].items():
            self._download_page(manga, chapter, page, img_url, chapter_dir)

    def _download_page(self, manga, chapter, page, img_url, chapter_dir):
        filepath = self._build_page_filepath(chapter_dir, page, img_url)
        self._stream_remote_image(img_url, filepath)

    def _build_page_filepath(self, directory, page, download_url):
        filetype = download_url.split('.')[-1]
        filename = f'{page}.{filetype}'
        return os.path.join(directory, filename)

    def _stream_remote_image(self, url, filepath):
        stream = requests.get(url, stream=True)
        stream.raise_for_status()
        self._stream_image_to_file(stream, filepath)

    def _stream_image_to_file(self, stream, filepath):
        with open(filepath, 'wb') as image_file:
            for chunk in stream.iter_content(1024):
                image_file.write(chunk)
