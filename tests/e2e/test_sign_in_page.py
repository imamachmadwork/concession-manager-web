import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_sign_in_page_loads(sign_in_page):
    sign_in_page.load()
    expect(sign_in_page.heading).to_be_visible()
    expect(sign_in_page.email_input).to_be_visible()
    expect(sign_in_page.password_input).to_be_visible()
    expect(sign_in_page.sign_in_button).to_be_visible()
