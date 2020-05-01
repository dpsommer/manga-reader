import re

import requests

from .source import Source
from ..manga import Manga, Chapter, Page


class MangaReader(Source):

    BASE_URL = 'http://www.mangareader.net'

    def get_chapters(self, title):
        url = f"{self.BASE_URL}/{title}"
        resp = requests.get(url)
        resp.raise_for_status()
        pattern = 'href="\\/{}\\/([\\d.]+)"'.format(title)
        chapters = re.findall(pattern, resp.text)
        return [Chapter(chapter, pages=self.get_pages(title, chapter)) for chapter in chapters]

    def get_pages(self, title, chapter):
        pages = range(1, self._get_page_count(title, chapter) + 1)
        return [Page(page, self._get_page_url(title, chapter, page)) for page in pages]

    def _get_page_count(self, title, chapter):
        url = f"{self.BASE_URL}/{title}/{chapter}"
        resp = requests.get(url)
        resp.raise_for_status()
        match = re.search(r'select>\s+of\s+(\d+)', resp.text)
        return int(match[1])

    def _get_page_url(self, title, chapter, page):
        url = f"{self.BASE_URL}/{title}/{chapter}"
        if int(page) > 1:  # special case - mangareader first page has no page # in url
            url += f"/{page}"
        resp = requests.get(url)
        resp.raise_for_status()
        match = re.search(r'id="img".+?src="(.*?)"\s+alt', resp.text)
        return match[1]

    def crawl(self):
        list_url = self._get_manga_list_url()
        resp = requests.get(list_url)
        resp.raise_for_status()
        titles = self._parse_manga_list(resp.text)
        return self._parse_title_list(titles)

    def _get_manga_list_url(self):
        return f"{self.BASE_URL}/alphabetical"

    def _parse_manga_list(self, page_content):
        # lstrip the page header and content before the series list
        page_content = page_content[page_content.find('series_alpha'):]
        pattern = r'<li>\s*<a href="\/([\w\d-]+)">.+?<\/a>'
        return re.findall(pattern, page_content)

    def _parse_title_list(self, titles):
        parser = MangaReaderDocumentParser()
        documents = []
        for title in titles:
            try:
                document = parser.parse(title)
                documents.append(document)
            except Exception as e:
                print(str(e))
        return documents


class MangaReaderDocumentParser(object):

    def __init__(self):
        self.page_content = None

    def parse(self, title):
        self._get_page_content(title)
        title = self._parse_title()
        return Manga.document(
            title=title,
            author=self._parse_author(),
            artist=self._parse_artist(),
            description=self._parse_description(),
            tags=self._parse_tags(),
            completed=self._parse_completion_status()
        )

    def _get_page_content(self, title):
        resp = requests.get(f'{MangaReader.BASE_URL}/{title}')
        resp.raise_for_status()
        self.page_content = resp.text

    def _parse_title(self):
        return re.search(r'<h2\s+class="aname">(.+?)<\/h2>', self.page_content)[1].strip()

    def _parse_author(self):
        author = re.search(r'<td\s+class="propertytitle">Author:<\/td>\s+<td>(.*?)<\/td>', self.page_content)[1]
        author = self._sanitize_author_or_artist_field(author)
        return author.strip()

    def _parse_artist(self):
        artist = re.search(r'<td\s+class="propertytitle">Artist:<\/td>\s+<td>(.*?)<\/td>', self.page_content)[1]
        artist = self._sanitize_author_or_artist_field(artist)
        return artist.strip()

    def _sanitize_author_or_artist_field(self, field):
        field = re.sub(r"[\(\[].*?[\)\]]", "", field)
        field = field.replace(',', '')
        return field.lower().strip()

    def _parse_description(self):
        description = re.search(r'<div\s+id="readmangasum">[\s\S]*?<p>([\s\S]*?)<\/p>', self.page_content)[1]
        description = re.sub(r'\s{2,}', ' ', description)
        return description.strip()

    def _parse_tags(self):
        return re.findall(r'<span\s+class="genretags">([\w\s-]+)<\/span>', self.page_content)

    def _parse_completion_status(self):
        completed = re.search(r'<td\s+class="propertytitle">Status:<\/td>\s*<td>(\w*?)<\/td>', self.page_content)[1]
        return completed.lower() == 'completed'
