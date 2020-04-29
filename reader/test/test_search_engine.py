import pytest
from whoosh.filedb.filestore import RamStorage

from ..manga import MangaSchema
from ..search import SearchEngine


@pytest.fixture
def manga_documents():
    return [
        {
            "title": u"Junjou Drop",
            "author": u"NAKAHARA Aya",
            "artist": u"NAKAHARA Aya",
            "description": u"Recently rejected Saki Momota is having a hard time getting over her first love. While picking up her younger brother from school, Saki bumps into Akai Ryuuichi; the class delinquent whos rumored to be able to shoot lazer-beams from his eyes. Could this day get any worse?",
            "tags": u"comedy,romance,shoujo",
            "completed": True,
            "url": u"http://www.mangareader.net/junjou-drop"
        },
        {
            "title": u"Ultraman",
            "author": u"SHIMIZU Eiichi, SHIMOGUCHI Tomohiro",
            "artist": u"SHIMIZU Eiichi, SHIMOGUCHI Tomohiro",
            "description": u"It has been years since Earth has seen and needed ULTRAMAN. The world has forgotten its mighty champion. Jiro Shin, son of Hayata Shin, is a high school student who has always wanted to a hero like ULTRAMAN. One fateful day, however, a special high-tech suit will ensure his fate to become the legendary hero.",
            "tags": u"action,mystery,sci-fi,seinen,supernatural",
            "completed": False,
            "url": u"http://www.mangareader.net/ultraman"
        },
        {
            "title": u"Ito Junji's Cat Diary",
            "author": u"ITOU Junji",
            "artist": u"ITOU Junji",
            "description": u"Horror manga author Mr. J moves into his new house with his fiancée A-ko. Much to his chagrin, she brings two guests with her.",
            "tags": u"comedy,seinen,slice of life",
            "completed": False,
            "url": u"http://www.mangareader.net/ito-junjis-cat-diary"
        },
        {
            "title": u"Junjou Karen na Oretachi da",
            "author": None,
            "artist": None,
            "description": u"A pretty-boy volleyball player named Akira gets kicked out of his middle school team for being too arrogant. With his coach refusing to give him a reference, it looks like he will only be able to go to a high school with a mediocre volleyball team. By chance, he finds a leaflet for Seiryoh High School volleyball team and decided to try out. But then complications arise in the form of a delinquent with very curly hair.",
            "tags": u"action,shounen,sports",
            "completed": True,
            "url": u"http://www.mangareader.net/junjou-karen-na-oretachi-da"
        },
        {
            "title": u"Clover (TETSUHIRO Hirakawa)",
            "author": u"TETSUHIRO Hirakawa",
            "artist": u"TETSUHIRO Hirakawa",
            "description": u"Three childhood friends are meeting again in high school. Hayato (see cover) the crazy one, Kenji the big one who wouldn't hurt a fly, and Tomoki the solitary one are the main characters of this fighting manga.",
            "tags": u"action,comedy,shounen",
            "completed": False,
            "url": u"http://www.mangareader.net/clover-tetsuhiro-hirakawa"
        },
        {
            "title": u"Ranma 1/2",
            "author": u"TAKAHASHI Rumiko",
            "artist": u"TAKAHASHI Rumiko",
            "description": u"Being a teenage martial artist isn't easy, especially for Ranma Saotome, who went through a major transformation on a training mission with his father. After an accidental dunk into a legendary cursed spring in China, Ranma now changes into a girl every time he's splashed with cold water. That would be enough to complicate anyone's life, even without the arranged fiancée who doesn't like him (or says she doesn't) and the constant stream of rivals and suitors for both his male and female forms. What's a half-guy, half-girl to do?",
            "tags": u"action,comedy,gender bender,harem,martial arts,romance,school life,shounen",
            "completed": True,
            "url": u"http://www.mangareader.net/ranma-12"
        },
        {
            "title": u"Mahou Sensei Negima!",
            "author": u"AKAMATSU Ken",
            "artist": u"AKAMATSU Ken",
            "description": u"After graduated from a magic academy, 10-year-old genius boy Negi Springfield was assigned to a huge Japanese school as an English teacher for practical training. To his surprise, the 8th grade class assigned for him is all-girl. In addition to teaching (and being teased by) those 31 pretty girls while trying to keep his magic capability in secret, he's also looking for clues about his father, who was once known as \"Thousand Master\" but mysteriously disappeared years ago.",
            "tags": u"action,comedy,ecchi,fantasy,harem,magic,shounen,supernatural",
            "completed": True,
            "url": u"http://www.mangareader.net/mahou-sensei-negima"
        },
        {
            "title": u"Vagabond",
            "author": u"INOUE Takehiko, YOSHIKAWA Eiji",
            "artist": u"INOUE Takehiko",
            "description": u"Shinmen Takezo is destined to become the legendary sword-saint, Miyamoto Musashi--perhaps the most renowned samurai of all time. For now, Takezo is a cold-hearted kiler, who will take on anyone in mortal combat to make a name for himself. This is the journey of a wild young brute who strives to reach enlightenment by way of the sword--fighting on the edge of death.",
            "tags": u"action,drama,historical,martial arts,mature,seinen",
            "completed": False,
            "url": u"http://www.mangareader.net/vagabond"
        }
    ]


@pytest.fixture
def index():
    storage = RamStorage()
    index = storage.create_index(MangaSchema)
    yield index
    index.close()


@pytest.fixture
def search_engine(mocker, index, manga_documents):
    mocker.patch('reader.search.search_engine.SearchEngine._load_index', return_value=index)
    search_engine = SearchEngine()
    search_engine.index(manga_documents)
    return search_engine


def test_exact_match_search(search_engine):
    results = search_engine.search('Junjou')
    assert results[0]['title'] == 'Junjou Drop'
    assert len(results) == 2
