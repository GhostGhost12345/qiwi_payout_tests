import pytest
from playwright.sync_api import sync_playwright

from config import TOKEN, BASE_URL, validate_config
from qiwi_api_client import QiwiApiClient


validate_config()


@pytest.fixture(scope="session")
def playwright_context():
    with sync_playwright() as p:
        yield p


@pytest.fixture
def api_client(playwright_context):
    client = QiwiApiClient(playwright_context, TOKEN, BASE_URL)
    yield client
    client.dispose()
