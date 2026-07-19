import pytest


@pytest.fixture
def sign_in_page(page):
    from pages.sign_in_page import SignInPage

    return SignInPage(page)


# --- Authenticated-session pattern (example — adapt or delete) -------------
#
# For apps that need sign-in, driving the login UI in every test is slow and
# often trips rate limits. Sign in once per session, capture Playwright's
# storage_state (cookies/localStorage), and hand out fresh pages seeded with
# it instead. Adapt SignInPage/URLs to the actual app, then reuse this shape
# for any fixture that needs to start authenticated:
#
# @pytest.fixture(scope="session")
# def default_storage_state(browser, base_url):
#     from credentials import get_credentials
#     from pages.sign_in_page import SignInPage
#
#     creds = get_credentials("default")
#     context = browser.new_context(base_url=base_url)
#     page = context.new_page()
#
#     sign_in_page = SignInPage(page)
#     sign_in_page.load()
#     sign_in_page.sign_in(email=creds["email"], password=creds["password"])
#     page.wait_for_url("**/dashboard")
#
#     state = context.storage_state()
#     context.close()
#     return state
#
#
# @pytest.fixture
# def authenticated_page(browser, default_storage_state):
#     context = browser.new_context(storage_state=default_storage_state)
#     page = context.new_page()
#     yield page
#     context.close()
