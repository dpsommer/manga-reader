from whoosh.fields import SchemaClass, TEXT, KEYWORD, BOOLEAN, ID


class MangaSchema(SchemaClass):
    title = TEXT(stored=True)
    author = TEXT(stored=True)
    artist = TEXT(stored=True)
    description = TEXT  # TODO: should the description be stored separately?
    tags = KEYWORD(stored=True, lowercase=True, commas=True, scorable=True)
    completed = BOOLEAN
    url = ID(stored=True)


class Manga(object):

    def __init__(self,
                 title: str, chapters: dict,
                 author='', artist='', description='',
                 tags=[], completed=False):
        self.title = title
        self.chapters = chapters
        self.author = author
        self.artist = artist
        self.description = description
        self.tags = tags
        self.completed = completed

    def as_document(self):
        return {
            'title': self.title.encode(),
            'author': self.author.encode(),
            'artist': self.artist.encode(),
            'description': self.description.encode(),
            'tags': ','.join(self.tags).encode(),
            'completed': self.completed
        }
