.PHONY: init test coverage ci

init:
	pip install -r requirements.txt tox

test:
	tox

coverage:
	pytest --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=mangareader tests

ci:
	pytest tests --junitxml=report.xml
