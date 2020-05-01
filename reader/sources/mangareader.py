import re

import requests

from .source import Source, DocumentParser
from ..manga import Manga, Chapter, Page


class MangaReaderDocumentParser(DocumentParser):

    def _get_page_content(self, title):
        resp = requests.get(self.context.url or self._get_url(title))
        resp.raise_for_status()
        return resp.text

    def _get_url(self, title):
        return f'{MangaReader.BASE_URL}/{title}'

    def _parse_title(self):
        return re.search(r'<h2\s+class="aname">(.+?)<\/h2>', self.context.page_content)[1].strip()

    def _parse_author(self):
        author = re.search(r'<td\s+class="propertytitle">Author:<\/td>\s+<td>(.*?)<\/td>', self.context.page_content)[1]
        author = self._sanitize_author_or_artist_field(author)
        return author.strip()

    def _parse_artist(self):
        artist = re.search(r'<td\s+class="propertytitle">Artist:<\/td>\s+<td>(.*?)<\/td>', self.context.page_content)[1]
        artist = self._sanitize_author_or_artist_field(artist)
        return artist.strip()

    def _sanitize_author_or_artist_field(self, field):
        field = re.sub(r"[\(\[].*?[\)\]]", "", field)
        field = field.replace(',', '')
        return field.lower().strip()

    def _parse_description(self):
        description = re.search(r'<div\s+id="readmangasum">[\s\S]*?<p>([\s\S]*?)<\/p>', self.context.page_content)[1]
        description = re.sub(r'\s{2,}', ' ', description)
        return description.strip()

    def _parse_tags(self):
        tags = re.findall(r'<span\s+class="genretags">([\w\s-]+)<\/span>', self.context.page_content)
        return ','.join(tags)

    def _parse_completion_status(self):
        completed = re.search(r'<td\s+class="propertytitle">Status:<\/td>\s*<td>(\w*?)<\/td>', self.context.page_content)[1]
        return completed.lower() == 'completed'


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

    def get_manga_list(self):
        list_url = f"{self.BASE_URL}/alphabetical"
        resp = requests.get(list_url)
        resp.raise_for_status()
        return self._parse_manga_list(resp.text)

    def _parse_manga_list(self, page_content):
        # lstrip the page header and content before the series list
        page_content = page_content[page_content.find('series_alpha'):]
        pattern = r'<li>\s*<a href="\/([\w\d-]+)">.+?<\/a>'
        return re.findall(pattern, page_content)

    def _get_document_parser(self, context):
        return MangaReaderDocumentParser(context)
