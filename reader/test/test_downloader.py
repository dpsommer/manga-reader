import os

import pytest
from requests_mock import ANY

from ..utils import Downloader
from ..manga import Manga, Chapter, Page
from .common import DIRPATH, clean_tree

TEST_DATA_DIR = os.path.join(DIRPATH, 'test_downloads')
IMAGE_URL = 'https://example.com/123.jpg'


@pytest.fixture(scope='module')
def test_manga():
    return Manga('fuuka', chapters=[
        Chapter(1, pages=[
            Page(1, 'https://i1.imggur.net/fuuka/1/fuuka-4791557.jpg'),
            Page(2, 'https://i7.imggur.net/fuuka/1/fuuka-4791559.jpg')
        ])
    ])


@pytest.fixture
def downloader(mocker):
    yield Downloader(manga_home=TEST_DATA_DIR)
    clean_tree(TEST_DATA_DIR)


def test_download_manga(mocker, requests_mock, downloader, test_manga):
    mocker.patch('reader.sources.mangareader.MangaReaderScraper._get_page_url', return_value=IMAGE_URL)
    requests_mock.get(ANY, content=b'some test content')
    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    downloader.download_manga(test_manga)
    # get last page for assert_called_with
    page_file = page_file = os.path.join(TEST_DATA_DIR, 'fuuka', '1', '2.jpg')
    mock_open.assert_called_with(page_file, 'wb')
    assert os.path.isdir(TEST_DATA_DIR)


def test_download_chapter(mocker, downloader, test_manga):
    mocker.patch('reader.utils.downloader.Downloader._ChapterDownloader._download_page')
    chapter = test_manga.chapters[0]
    downloader.download_chapter(test_manga.title, chapter)
    assert os.path.isdir(TEST_DATA_DIR)


def test_skip_download_if_chapter_exists(mocker, downloader, test_manga):
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('reader.utils.downloader.Downloader._ChapterDownloader._download_page', side_effect=Exception)
    downloader.download_manga(test_manga)


@pytest.mark.functional
def test_download(downloader, test_manga):
    downloader.download_manga(test_manga)
    page_file = os.path.join(TEST_DATA_DIR, 'fuuka', '1', '1.jpg')
    assert os.stat(page_file).st_size > 0
