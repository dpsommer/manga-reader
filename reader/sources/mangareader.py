import re

import requests
from bs4 import BeautifulSoup

from .source import Source, Scraper, DocumentParser

BASE_URL = 'http://www.mangareader.net'
HTML_PARSER = 'lxml'


class MangaReaderDocumentParser(DocumentParser):

    def _get_page_parser(self, title):
        resp = requests.get(self.context.url or self._get_url(title))
        resp.raise_for_status()
        return BeautifulSoup(resp.text, HTML_PARSER)

    def _get_url(self, title):
        return f'{BASE_URL}/{title}'

    def _parse_title(self):
        return self.context.parser.find('h2', class_='aname').string

    def _parse_author(self):
        author = self._get_property('author')
        author = self._sanitize_author_or_artist_field(author)
        return author.strip()

    def _parse_artist(self):
        artist = self._get_property('artist')
        artist = self._sanitize_author_or_artist_field(artist)
        return artist.strip()

    def _sanitize_author_or_artist_field(self, field):
        field = re.sub(r"[\(\[].*?[\)\]]", "", field)
        field = field.replace(',', '')
        return field.lower().strip()

    def _parse_description(self):
        summary = self.context.parser.find(id='readmangasum')
        description = summary.p.string
        description = re.sub(r'\s{2,}', ' ', description)
        return description.strip()

    def _parse_tags(self):
        tags = self.context.parser('span', class_='genretags')
        tags = [tag.string.strip() for tag in tags]
        return ','.join(tags)

    def _parse_completion_status(self):
        completed = self._get_property('status')
        return completed.lower() == 'completed'

    def _get_property(self, prop):

        if not hasattr(self.context, 'properties'):
            self.context.properties = self._parse_properties()
        return self.context.properties[prop]

    def _parse_properties(self):
        properties = {}
        props = self.context.parser.find_all('td', class_='propertytitle')
        for prop in props:
            prop_name = prop.string.strip().replace(':', '').lower()
            properties[prop_name] = prop.find_next_sibling('td').string
        return properties


class MangaReaderScraper(Scraper):

    def get_chapters(self):
        url = f"{BASE_URL}/{self.title}"
        resp = requests.get(url)
        resp.raise_for_status()
        parser = BeautifulSoup(resp.text, HTML_PARSER)
        link_tags = parser.find_all('a', href=re.compile('^/{}'.format(self.title)))
        return [tag['href'].split('/')[-1] for tag in link_tags]

    def _get_page_count(self, chapter):
        url = f"{BASE_URL}/{self.title}/{chapter}"
        resp = requests.get(url)
        resp.raise_for_status()
        parser = BeautifulSoup(resp.text, HTML_PARSER)
        options = parser.find(id='selectpage')('option')
        return int(options[-1].string)

    def _get_page_url(self, chapter, page):
        url = f"{BASE_URL}/{self.title}/{chapter}"
        if int(page) > 1:  # special case - mangareader first page has no page # in url
            url += f"/{page}"
        resp = requests.get(url)
        resp.raise_for_status()
        parser = BeautifulSoup(resp.text, HTML_PARSER)
        return parser.find(id='img')['src']


class MangaReader(Source):

    def get_scraper(self, title):
        return MangaReaderScraper(self.normalize(title))

    @staticmethod
    def normalize(input_str):
        output = re.sub('[^A-Za-z0-9 ]+', '', input_str)
        return output.replace(' ', '-').lower()

    def get_manga_list(self):
        list_url = f"{BASE_URL}/alphabetical"
        resp = requests.get(list_url)
        resp.raise_for_status()
        return self._parse_manga_list(resp.text)

    def _parse_manga_list(self, page_content):
        parser = BeautifulSoup(page_content, HTML_PARSER)
        series_lists = parser.find_all('ul', class_='series_alpha')
        manga_list = []
        for series_list in series_lists:
            all_series = series_list.find_all('a')
            for series in all_series:
                manga_list.append(series['href'][1:])  # strip leading /
        return manga_list

    def get_document_parser(self, context):
        return MangaReaderDocumentParser(context)
