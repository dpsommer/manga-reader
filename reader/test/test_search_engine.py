import os

import pytest
from whoosh.filedb.filestore import RamStorage

from ..manga import MangaSchema
from ..search import SearchEngine
from .common import DIRPATH, clean_tree

TEST_INDEX_DIR = os.path.join(DIRPATH, 'test_index')


@pytest.fixture(scope='module')
def manga_documents():
    return [
        {
            "title": "Junjou Drop",
            "author": "NAKAHARA Aya",
            "artist": "NAKAHARA Aya",
            "description": "Recently rejected Saki Momota is having a hard time getting over her first love. While picking up her younger brother from school, Saki bumps into Akai Ryuuichi; the class delinquent whos rumored to be able to shoot lazer-beams from his eyes. Could this day get any worse?",
            "tags": "comedy,romance,shoujo",
            "completed": True,
            "url": "http://www.mangareader.net/junjou-drop"
        },
        {
            "title": "Ultraman",
            "author": "SHIMIZU Eiichi, SHIMOGUCHI Tomohiro",
            "artist": "SHIMIZU Eiichi, SHIMOGUCHI Tomohiro",
            "description": "It has been years since Earth has seen and needed ULTRAMAN. The world has forgotten its mighty champion. Jiro Shin, son of Hayata Shin, is a high school student who has always wanted to a hero like ULTRAMAN. One fateful day, however, a special high-tech suit will ensure his fate to become the legendary hero.",
            "tags": "action,mystery,sci-fi,seinen,supernatural",
            "completed": False,
            "url": "http://www.mangareader.net/ultraman"
        },
        {
            "title": "Ito Junji's Cat Diary",
            "author": "ITOU Junji",
            "artist": "ITOU Junji",
            "description": "Horror manga author Mr. J moves into his new house with his fiancée A-ko. Much to his chagrin, she brings two guests with her.",
            "tags": "comedy,seinen,slice of life",
            "completed": False,
            "url": "http://www.mangareader.net/ito-junjis-cat-diary"
        },
        {
            "title": "Junjou Karen na Oretachi da",
            "author": None,
            "artist": None,
            "description": "A pretty-boy volleyball player named Akira gets kicked out of his middle school team for being too arrogant. With his coach refusing to give him a reference, it looks like he will only be able to go to a high school with a mediocre volleyball team. By chance, he finds a leaflet for Seiryoh High School volleyball team and decided to try out. But then complications arise in the form of a delinquent with very curly hair.",
            "tags": "action,shounen,sports",
            "completed": True,
            "url": "http://www.mangareader.net/junjou-karen-na-oretachi-da"
        },
        {
            "title": "Clover (TETSUHIRO Hirakawa)",
            "author": "TETSUHIRO Hirakawa",
            "artist": "TETSUHIRO Hirakawa",
            "description": "Three childhood friends are meeting again in high school. Hayato (see cover) the crazy one, Kenji the big one who wouldn't hurt a fly, and Tomoki the solitary one are the main characters of this fighting manga.",
            "tags": "action,comedy,shounen",
            "completed": False,
            "url": "http://www.mangareader.net/clover-tetsuhiro-hirakawa"
        },
        {
            "title": "Ranma 1/2",
            "author": "TAKAHASHI Rumiko",
            "artist": "TAKAHASHI Rumiko",
            "description": "Being a teenage martial artist isn't easy, especially for Ranma Saotome, who went through a major transformation on a training mission with his father. After an accidental dunk into a legendary cursed spring in China, Ranma now changes into a girl every time he's splashed with cold water. That would be enough to complicate anyone's life, even without the arranged fiancée who doesn't like him (or says she doesn't) and the constant stream of rivals and suitors for both his male and female forms. What's a half-guy, half-girl to do?",
            "tags": "action,comedy,gender bender,harem,martial arts,romance,school life,shounen",
            "completed": True,
            "url": "http://www.mangareader.net/ranma-12"
        },
        {
            "title": "Mahou Sensei Negima!",
            "author": "AKAMATSU Ken",
            "artist": "AKAMATSU Ken",
            "description": "After graduated from a magic academy, 10-year-old genius boy Negi Springfield was assigned to a huge Japanese school as an English teacher for practical training. To his surprise, the 8th grade class assigned for him is all-girl. In addition to teaching (and being teased by) those 31 pretty girls while trying to keep his magic capability in secret, he's also looking for clues about his father, who was once known as \"Thousand Master\" but mysteriously disappeared years ago.",
            "tags": "action,comedy,ecchi,fantasy,harem,magic,shounen,supernatural",
            "completed": True,
            "url": "http://www.mangareader.net/mahou-sensei-negima"
        },
        {
            "title": "Vagabond",
            "author": "INOUE Takehiko, YOSHIKAWA Eiji",
            "artist": "INOUE Takehiko",
            "description": "Shinmen Takezo is destined to become the legendary sword-saint, Miyamoto Musashi--perhaps the most renowned samurai of all time. For now, Takezo is a cold-hearted kiler, who will take on anyone in mortal combat to make a name for himself. This is the journey of a wild young brute who strives to reach enlightenment by way of the sword--fighting on the edge of death.",
            "tags": "action,drama,historical,martial arts,mature,seinen",
            "completed": False,
            "url": "http://www.mangareader.net/vagabond"
        }
    ]


@pytest.fixture
def index():
    storage = RamStorage()
    index = storage.create_index(MangaSchema)
    yield index
    index.close()


@pytest.fixture
def mock_search_engine(mocker, index, manga_documents):
    mocker.patch('reader.search.search_engine.SearchEngine._load_index', return_value=index)
    search_engine = SearchEngine()
    search_engine.index(manga_documents)
    return search_engine


@pytest.mark.functional
@pytest.fixture(scope='module')
def search_engine(manga_documents):
    search_engine = SearchEngine(index_path=TEST_INDEX_DIR)
    search_engine.index(manga_documents)
    yield search_engine
    clean_tree(TEST_INDEX_DIR)


def test_exact_match_search(mock_search_engine):
    results = mock_search_engine.search('Junjou')
    assert results[0]['title'] == 'Junjou Drop'
    assert len(results) == 2


@pytest.mark.functional
def test_load_index(search_engine):
    se = SearchEngine(index_path=TEST_INDEX_DIR)
    assert se._index.doc_count() == search_engine._index.doc_count()


@pytest.mark.functional
def test_search_filesystem_index(search_engine):
    results = search_engine.search('Junjou')
    assert results[0]['title'] == 'Junjou Drop'
