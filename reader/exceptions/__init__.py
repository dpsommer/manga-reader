class MangaReaderException(Exception):

    ERROR_MESSAGE = ''

    def __init__(self, message=''):
        super().__init__(message or self.ERROR_MESSAGE)


class NoSuchSource(MangaReaderException):
    ERROR_MESSAGE = 'No such source'
