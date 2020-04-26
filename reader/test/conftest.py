import pytest


def pytest_addoption(parser):
    parser.addoption('--functional', action='store_true', help="Functional flag to run integration tests")


def pytest_runtest_setup(item):
    if 'functional' in item.keywords and not item.config.getoption('--functional'):
        pytest.skip("Use the --functional flag to run functional tests")
