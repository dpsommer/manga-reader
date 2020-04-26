import os

import requests

from ..sources import MangaReader, Source

HOME_DIRECTORY = os.path.expanduser('~')
MANGA_DOWNLOAD_DIRECTORY = os.getenv('MANGA_HOME', os.path.join(HOME_DIRECTORY, 'manga'))


class Downloader(object):

    def __init__(self, source: Source = MangaReader, manga_home=MANGA_DOWNLOAD_DIRECTORY):
        self.source = source()
        self.manga_home = manga_home

    def download_manga(self, title):
        manga = self.source.get_manga(title)
        for chapter in manga.chapters.keys():
            chapter_dir = self._build_chapter_dirpath(manga, chapter)
            if not os.path.exists(chapter_dir):
                self.download_chapter(manga, chapter, chapter_dir)

    def _build_chapter_dirpath(self, manga, chapter):
        return os.path.join(self.manga_home, manga.title, str(chapter))

    def download_chapter(self, manga, chapter, chapter_dir=None):
        chapter_dir = chapter_dir or self._build_chapter_dirpath(manga, chapter)
        os.makedirs(chapter_dir, exist_ok=True)
        for page in manga.chapters[chapter]:
            self._download_page(manga, chapter, page, chapter_dir)

    def _download_page(self, manga, chapter, page, chapter_dir):
        img_url = self.source.get_page_url(manga.title, chapter, page)
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
