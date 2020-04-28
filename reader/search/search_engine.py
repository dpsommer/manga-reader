import os
from abc import ABC

from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import QueryParser

from ..manga import MangaSchema
from ..utils import ROOT_DIRECTORY

INDEX_DIRECTORY = os.path.join(ROOT_DIRECTORY, 'index')


class SearchEngine(object):

    def __init__(self, index_name='default', schema=None):
        self._index = self._load_index(index_name)
        self._schema = schema or MangaSchema

    def index(self, data) -> None:
        # NB: consider using multisegment=True here for initial indexing
        w = self._index.writer(limitmb=512)
        for document in data:
            w.add_document(**document)
        w.commit()

    def _load_index(self, index_name):
        if exists_in(INDEX_DIRECTORY, indexname=index_name):
            return open_dir(INDEX_DIRECTORY, indexname=index_name)
        return create_in(INDEX_DIRECTORY, self._schema, indexname=index_name)

    def search(self, search_string: str) -> list:
        results = []
        with self._index.searcher() as searcher:
            parser = QueryParser("title", self._index.schema)
            query = parser.parse(search_string.encode())
            search_results = searcher.search(query)
            for result in search_results:
                results.append(dict(result))
        return results
