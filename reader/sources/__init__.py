from .source import Source
from .mangareader import MangaReader, MangaReaderDocumentParser
from ..exceptions import NoSuchSource


class SourceFactory(object):

    @staticmethod
    def instance(source):
        source = source.lower()
        if source == 'mangareader':
            return MangaReader()
        raise NoSuchSource()
