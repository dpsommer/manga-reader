from inspect import isclass

from .source import Source
from .mangareader import MangaReader, MangaReaderDocumentParser
from ..exceptions import NoSuchSource

SOURCES = {MangaReader}


class SourceFactory(object):

    @staticmethod
    def instance(source):
        if isclass(source):
            if source in SOURCES:
                return source()
            raise TypeError("Invalid source type")
        source = source.lower()
        if source == 'mangareader':
            return MangaReader()
        raise NoSuchSource()
