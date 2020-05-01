import os
import shutil

import pytest
from requests_mock import ANY

from ..utils import Downloader
from ..sources import MangaReader
from ..manga import Manga, Chapter, Page

DIRPATH = os.path.abspath(os.path.dirname(__file__))
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
    chapter = test_manga.chapters[0]
    page = chapter.pages[-1]  # get last page for assert_called_with
    page_file = downloader._build_page_filepath(page)
    mock_open.assert_called_with(page_file, 'wb')
    assert os.path.isdir(TEST_DATA_DIR)


def test_download_chapter(mocker, downloader, test_manga):
    mocker.patch('reader.utils.downloader.Downloader._download_page')
    chapter = test_manga.chapters[0]
    downloader.download_chapter(test_manga, chapter)
    assert os.path.isdir(TEST_DATA_DIR)


def test_error_if_no_chapter_dir_set(downloader, test_manga):
    page = test_manga.chapters[0].pages[0]
    with pytest.raises(Exception):
        downloader._download_page(page)

def test_skip_download_if_chapter_exists(mocker, downloader, test_manga):
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('reader.utils.downloader.Downloader.download_chapter', side_effect=Exception)
    downloader.download_manga(test_manga)


@pytest.mark.functional
def test_download(downloader, test_manga):
    chapter = test_manga.chapters[0]
    page = chapter.pages[0]
    downloader.download_manga(test_manga)
    page_file = downloader._build_page_filepath(page)
    assert os.stat(page_file).st_size > 0
