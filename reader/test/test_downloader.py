import os
import shutil

import pytest
from requests_mock import ANY

from ..utils import Downloader
from ..sources import MangaReader
from ..manga import Manga

DIRPATH = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(DIRPATH, 'data')
IMAGE_URL = 'https://example.com/123.jpg'


@pytest.fixture(scope='module')
def test_manga():
    return Manga('fuuka', {
        1: {
            1: 'https://i1.imggur.net/fuuka/1/fuuka-4791557.jpg',
            2: 'https://i7.imggur.net/fuuka/1/fuuka-4791559.jpg'
        }
    })


@pytest.fixture
def downloader(mocker, test_manga):
    yield Downloader(manga_home=TEST_DATA_DIR)
    if os.path.isdir(TEST_DATA_DIR):
        for filename in os.listdir(TEST_DATA_DIR):  # teardown
            file_path = os.path.join(TEST_DATA_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        os.rmdir(TEST_DATA_DIR)


def test_download_manga(mocker, requests_mock, downloader, test_manga):
    mocker.patch('reader.sources.MangaReader._get_page_url', return_value=IMAGE_URL)
    requests_mock.get(ANY, content=b'some test content')
    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    downloader.download_manga(test_manga)
    chapter = list(test_manga.chapters.keys())[0]
    page = list(test_manga.chapters[chapter].keys())[-1]  # get last page for assert_called_with
    chapter_dir = os.path.join(TEST_DATA_DIR, test_manga.title, str(chapter))
    page_file = downloader._build_page_filepath(chapter_dir, page, IMAGE_URL)
    mock_open.assert_called_with(page_file, 'wb')
    assert os.path.isdir(TEST_DATA_DIR)


def test_download_chapter(mocker, downloader, test_manga):
    mocker.patch('reader.utils.downloader.Downloader._download_page')
    chapter = list(test_manga.chapters.keys())[0]
    downloader.download_chapter(test_manga, chapter)
    assert os.path.isdir(TEST_DATA_DIR)


def test_skip_download_if_chapter_exists(mocker, downloader, test_manga):
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('reader.utils.downloader.Downloader.download_chapter', side_effect=Exception)
    downloader.download_manga(test_manga)


@pytest.mark.functional
def test_download(downloader, test_manga):
    chapter = list(test_manga.chapters.keys())[0]
    page = list(test_manga.chapters[chapter].keys())[0]
    downloader.download_manga(test_manga.title)
    chapter_dir = os.path.join(TEST_DATA_DIR, test_manga.title, str(chapter))
    img_url = downloader.source.get_page_url(test_manga.title, chapter, page)
    page_file = downloader._build_page_filepath(chapter_dir, page, img_url)
    assert os.stat(page_file).st_size > 0
