import re

import pytest

from ..manga import Manga
from ..sources import MangaReader

MANGA_TITLE = 'fuuka'
CHAPTER = 2
PAGE = 2
MANGA_LIST_CONTENT = """
<div class="series_col">
    <a name=" "></a>
    <div class="series_alpha">
        <h2 class="series_alpha"><a href="#top"> </a></h2>
        <ul class="series_alpha">
            <li>
                <a href="/ichiba-kurogane-wa-kasegitai"> Ichiba Kurogane wa Kasegitai</a>
                <span class="mangacompleted">[Completed]</span>
            </li>
            <li>
                <a href="/junjou-drop"> Junjou Drop</a>
                <span class="mangacompleted">[Completed]</span>
            </li>
            <li>
                <a href="/kanchigai-hime-to-usotsuki-shimobe"> Kanchigai Hime to Usotsuki Shimobe</a>
                <span class="mangacompleted">[Completed]</span>
            </li>
            <li>
                <a href="/musashi-kun-to-murayama-san-wa-tsukiatte-mita"> Musashi-kun to Murayama-san wa Tsukiatte Mita.</a>
            </li>
            <li>
                <a href="/tobaku-datenroku-kaiji-kazuyahen"> Tobaku Datenroku Kaiji: Kazuyahen</a>
            </li>
            <li>
                <a href="/welcome-to-ghost-city"> Welcome to Ghost City</a>
            </li>
        </ul>
        <div class="clear">
    </div>
</div>
"""
OVERVIEW_CONTENT = """
<div id="latestchapters">
    <div id="popularcaption">
        <h3>LATEST CHAPTERS</h3>
    </div>
    <ul><li>
        <div class="chico_manga"></div>
        <a href="/fuuka/152">Fuuka 152</a> : </li>
    </ul>
</div>
<div id="chapterlist">
    <table id="listing">
        <tr class="table_head">
            <th class="leftgap">Chapter Name</th>
            <th>Date Added</th>
        </tr>
        <tr>
            <td>
                <div class="chico_manga"></div>
                <a href="/fuuka/1">Fuuka 1</a> : </td>
            <td>02/10/2014</td>
        </tr>
        <tr>
            <td>
                <div class="chico_manga"></div>
                <a href="/fuuka/2">Fuuka 2</a> : </td>
            <td>02/15/2014</td>
        </tr>
    </table>
</div>
"""
FIRST_PAGE_CONTENT = """
<div id="selectpage">
    <select id="pageMenu" name="pageMenu"><option value="/fuuka/2" selected="selected">1</option>
        <option value="/fuuka/2/2">2</option>
        <option value="/fuuka/2/3">3</option>
        <option value="/fuuka/2/4">4</option>
        <option value="/fuuka/2/5">5</option>
        <option value="/fuuka/2/6">6</option>
        <option value="/fuuka/2/7">7</option>
        <option value="/fuuka/2/8">8</option>
        <option value="/fuuka/2/9">9</option>
        <option value="/fuuka/2/10">10</option>
        <option value="/fuuka/2/11">11</option>
        <option value="/fuuka/2/12">12</option>
        <option value="/fuuka/2/13">13</option>
        <option value="/fuuka/2/14">14</option>
        <option value="/fuuka/2/15">15</option>
        <option value="/fuuka/2/16">16</option>
        <option value="/fuuka/2/17">17</option>
        <option value="/fuuka/2/18">18</option>
        <option value="/fuuka/2/19">19</option>
        <option value="/fuuka/2/20">20</option>
        <option value="/fuuka/2/21">21</option>
        <option value="/fuuka/2/22">22</option>
        <option value="/fuuka/2/23">23</option>
        <option value="/fuuka/2/24">24</option>
        <option value="/fuuka/2/25">25</option>
    </select> of 25</div>
</div>
...
<div id="imgholder">
    <div id="zoomer" class="zoomimg zoomtop">+ Larger Image</div>
    <a href="/fuuka/2/2">
        <img id="img" width="800" height="759" src="https://i5.imggur.net/fuuka/2/fuuka-4798605.jpg" alt="Fuuka 2 - Page 1" />
    </a>
    <div class="zoomimg zoombottom">+ Larger Image</div>
</div>
"""
NTH_PAGE_CONTENT = """
<div id="imgholder">
    <div id="zoomer" class="zoomimg zoomtop">+ Larger Image</div>
    <a href="/fuuka/2/3">
        <img id="img" width="800" height="1154" src="https://i5.imggur.net/fuuka/2/fuuka-4798607.jpg" alt="Fuuka 2 - Page 2" />
    </a>
    <div class="zoomimg zoombottom">+ Larger Image</div>
</div>
"""


@pytest.fixture
def mangareader(requests_mock):
    source = MangaReader()
    overview_url = f"{source.BASE_URL}/{MANGA_TITLE}"
    first_page_url = re.compile("{}/\\d+".format(overview_url))
    nth_page_url = re.compile("{}/\\d+/\\d+".format(overview_url))
    requests_mock.get(overview_url, text=OVERVIEW_CONTENT)
    requests_mock.get(first_page_url, text=FIRST_PAGE_CONTENT)
    requests_mock.get(nth_page_url, text=NTH_PAGE_CONTENT)
    return source


def test_get_manga_object(mocker, mangareader):
    mocker.patch('reader.sources.MangaReader._get_page_count', return_value=2)
    manga = mangareader.get_manga(MANGA_TITLE)
    assert type(manga) == Manga
    assert manga.chapters == {
        '152': {
            1: 'https://i5.imggur.net/fuuka/2/fuuka-4798605.jpg',
            2: 'https://i5.imggur.net/fuuka/2/fuuka-4798607.jpg'
        },
        '1': {
            1: 'https://i5.imggur.net/fuuka/2/fuuka-4798605.jpg',
            2: 'https://i5.imggur.net/fuuka/2/fuuka-4798607.jpg'
        },
        '2': {
            1: 'https://i5.imggur.net/fuuka/2/fuuka-4798605.jpg',
            2: 'https://i5.imggur.net/fuuka/2/fuuka-4798607.jpg'
        }
    }


def test_get_chapters(mangareader):
    chapters = [chapter for chapter in mangareader._get_chapters(MANGA_TITLE)]
    assert chapters == ['152', '1', '2']


def test_get_page_count(mangareader):
    assert mangareader._get_page_count(MANGA_TITLE, CHAPTER) == 25


def test_get_image_url_for_first_page(mangareader):
    assert mangareader._get_page_url(MANGA_TITLE, CHAPTER, 1) == "https://i5.imggur.net/fuuka/2/fuuka-4798605.jpg"


def test_get_image_url_for_nth_page(mangareader):
    assert mangareader._get_page_url(MANGA_TITLE, CHAPTER, PAGE) == "https://i5.imggur.net/fuuka/2/fuuka-4798607.jpg"


def test_crawler(requests_mock, mangareader):
    pass
