import pytest
from whoosh.filedb.filestore import RamStorage

from ..manga import MangaSchema
from ..search import SearchEngine


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
