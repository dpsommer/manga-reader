import re

import requests

from .source import Source


class MangaReader(Source):

    BASE_URL = 'http://www.mangareader.net'

    def _get_page_url(self, title, chapter, page):
        url = f"{self.BASE_URL}/{title}/{chapter}"
        if int(page) > 1:  # special case - mangareader first page has no page # in url
            url += f"/{page}"
        resp = requests.get(url)
        resp.raise_for_status()
        match = re.search(r'id="img".+?src="(.*?)" alt', resp.text)
        return match[1]

    def _get_pages(self, title, chapter):
        return [page for page in range(1, self._get_page_count(title, chapter) + 1)]

    def _get_page_count(self, title, chapter):
        url = f"{self.BASE_URL}/{title}/{chapter}"
        resp = requests.get(url)
        resp.raise_for_status()
        match = re.search(r'select> of (\d+)', resp.text)
        return int(match[1])

    def _get_chapters(self, title):
        url = f"{self.BASE_URL}/{title}"
        resp = requests.get(url)
        resp.raise_for_status()
        pattern = 'href="\\/{}\\/([\\d.]+)"'.format(title)
        for chapter in re.findall(pattern, resp.text):
            yield chapter
