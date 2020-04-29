from whoosh.fields import SchemaClass, TEXT, KEYWORD, BOOLEAN, ID


class MangaSchema(SchemaClass):
    title = TEXT(stored=True)
    author = TEXT
    artist = TEXT
    description = TEXT
    tags = KEYWORD(lowercase=True, commas=True, scorable=True)
    completed = BOOLEAN
    url = ID(stored=True)


class Manga(object):

    def __init__(self,
                 title: str, chapters=[],
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


class Chapter(object):

    def __init__(self, number, pages=[]):
        self.number = number
        self.pages = pages

    def __eq__(self, o):
        return self.number == o.number and set(self.pages) == set(o.pages)


class Page(object):

    def __init__(self, number, image_url):
        self.number = number
        self.image_url = image_url

    def __eq__(self, o):
        return self.number == o.number and self.image_url == o.image_url

    def __hash__(self):
        return hash((self.number, self.image_url))
