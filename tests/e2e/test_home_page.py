import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_home_page_loads(home_page):
    home_page.load()
    expect(home_page.main_heading).to_be_visible()
