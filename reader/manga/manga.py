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

    def __init__(self, title: str, chapters=[]):
        self.title = title
        self.chapters = chapters

    @staticmethod
    def document(**kwargs):
        return {
            'title': kwargs["title"].encode(),
            'author': kwargs["author"].encode(),
            'artist': kwargs["artist"].encode(),
            'description': kwargs["description"].encode(),
            'tags': ','.join(kwargs["tags"]).encode(),
            'completed': kwargs["completed"]
        }


class Chapter(object):

    def __init__(self, number, pages=[]):
        self.number = int(number)
        self.pages = pages

    def __eq__(self, o):
        return self.number == o.number and set(self.pages) == set(o.pages)


class Page(object):

    def __init__(self, number, image_url):
        self.number = int(number)
        self.image_url = image_url

    def __eq__(self, o):
        return self.number == o.number and self.image_url == o.image_url

    def __hash__(self):
        return hash((self.number, self.image_url))
