# MangaReader  

Lightweight python CLI for indexing, searching, and downloading Manga from popular online sources.  

## Usage

```
Usage: manga [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  download  - 
  read      -
  search    -
  version   -
```

## Indexing  

Sources are scraped and indexed using [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) 

## Search  

## Downloads  

By default, chapters are downloaded to `~/.manga/manga/<title>`.  

## Contributing  

### Local installation  

To install the package after checking out the repo locally, run  

```
$ python -m venv venv
$ source venv/bin/activate
$ python -m pip install -r requirements.txt
$ python -m pip install -e ./ 
```

### Running the tests  

The reader uses the [pytest](https://pytest.org) unit testing framework and [pytest-cov](https://pypi.org/project/pytest-cov/) for code coverage. Tests can be run after installing the package locally with  

```
$ py.test
```

from the project root.
