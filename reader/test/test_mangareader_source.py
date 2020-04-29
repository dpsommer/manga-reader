import os
import re

import pytest

from ..manga import Manga, Chapter, Page
from ..sources import MangaReader, MangaReaderDocumentParser

MANGA_TITLE = 'fuuka'
CHAPTER = 2
PAGE = 2
DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'mangareader')
OVERVIEW_URL = f"{MangaReader.BASE_URL}/{MANGA_TITLE}"
LIST_URL = f"{MangaReader.BASE_URL}/alphabetical"
OVERVIEW_PAGE = 'overview.html'
MANGA_FIRST_PAGE = 'first_page.html'
MANGA_NTH_PAGE = 'nth_page.html'
LIST_PAGE = 'list.html'


@pytest.fixture(autouse=True)
def mock_mangareader_requests(requests_mock):
    first_page_url = re.compile("{}/\\d+".format(OVERVIEW_URL))
    nth_page_url = re.compile("{}/\\d+/\\d+".format(OVERVIEW_URL))
    for url, html_filename in [
        (OVERVIEW_URL, OVERVIEW_PAGE),
        (first_page_url, MANGA_FIRST_PAGE),
        (nth_page_url, MANGA_NTH_PAGE),
        (LIST_URL, LIST_PAGE)
    ]:
        with open(os.path.join(DATA_DIR, html_filename), 'r') as f:
            requests_mock.get(url, text=f.read())
    return True


@pytest.fixture
def mangareader():
    return MangaReader()


def test_get_manga_object(mocker, mangareader):
    mocker.patch('reader.sources.MangaReader._get_page_count', return_value=2)
    manga = mangareader.get_manga(MANGA_TITLE)
    assert type(manga) == Manga
    assert manga.chapters == [
        Chapter("152", [
            Page(1, 'https://i5.imggur.net/fuuka/2/fuuka-4798605.jpg'),
            Page(2, 'https://i5.imggur.net/fuuka/2/fuuka-4798607.jpg')
        ]),
        Chapter("1", [
            Page(1, 'https://i5.imggur.net/fuuka/2/fuuka-4798605.jpg'),
            Page(2, 'https://i5.imggur.net/fuuka/2/fuuka-4798607.jpg')
        ]),
        Chapter("2", [
            Page(1, 'https://i5.imggur.net/fuuka/2/fuuka-4798605.jpg'),
            Page(2, 'https://i5.imggur.net/fuuka/2/fuuka-4798607.jpg')
        ])
    ]


def test_get_chapters(mangareader):
    chapters = [chapter for chapter in mangareader._get_chapters(MANGA_TITLE)]
    assert chapters == ['152', '1', '2']


def test_get_page_count(mangareader):
    assert mangareader._get_page_count(MANGA_TITLE, CHAPTER) == 25


def test_get_image_url_for_first_page(mangareader):
    assert mangareader._get_page_url(MANGA_TITLE, CHAPTER, 1) == "https://i5.imggur.net/fuuka/2/fuuka-4798605.jpg"


def test_get_image_url_for_nth_page(mangareader):
    assert mangareader._get_page_url(MANGA_TITLE, CHAPTER, PAGE) == "https://i5.imggur.net/fuuka/2/fuuka-4798607.jpg"


def test_parse_manga_properties(mangareader):
    parser = MangaReaderDocumentParser()
    document = parser.parse(MANGA_TITLE)
    assert document == {
        'title': 'Fuuka',
        'author': 'seo kouji',
        'artist': 'seo kouji',
        'description': 'Yuu Haruna just moved into town and love to be on twitter. Out on his way to buy dinner he bumps into a mysterious girl, Fuuka Akitsuki, who breaks his phone thinking he was trying to take a picture of her panties. How will his new life change now?',
        'tags': ['School Life', 'Shoujo'],
        'completed': False
    }


def test_crawler(mangareader):
    assert len(mangareader.crawl()) == 1
