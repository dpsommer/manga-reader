import os
from abc import ABC

from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import QueryParser

from ..manga import MangaSchema
from ..utils import ROOT_DIRECTORY

INDEX_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'index')


class SearchEngine(object):

    def __init__(self, index_path=INDEX_DIRECTORY, index_name='default', schema=None):
        self._schema = schema or MangaSchema
        self._index = self._load_index(index_path, index_name)

    def index(self, data) -> None:
        # NB: consider using multisegment=True here for initial indexing
        # Not using procs to multithread as it breaks RamStorage (used in tests)
        w = self._index.writer(limitmb=512)
        for document in data:
            w.add_document(**document)
        w.commit()

    def _load_index(self, index_path, index_name):
        if exists_in(index_path, indexname=index_name):
            return open_dir(index_path, indexname=index_name)
        os.makedirs(index_path, exist_ok=True)
        return create_in(index_path, self._schema, indexname=index_name)

    def search(self, search_string: str) -> list:
        results = []
        with self._index.searcher() as searcher:
            parser = QueryParser("title", self._index.schema)
            query = parser.parse(search_string.encode())
            search_results = searcher.search(query)
            for result in search_results:
                results.append(dict(result))
        return results
