import pytest

from clients.api_client import ApiClient


@pytest.fixture
def api_client():
    with ApiClient() as client:
        yield client


# --- Authenticated-session pattern (example — adapt or delete) -------------
#
# Mirrors tests/e2e/conftest.py's authenticated_page: log in once per
# session via a direct API call (faster and less rate-limit-prone than
# re-authenticating per test), then apply the resulting token to api_client
# for tests that need an authenticated session.
#
# @pytest.fixture(scope="session")
# def session_token():
#     from credentials import get_credentials
#
#     creds = get_credentials("default")
#     with ApiClient() as client:
#         response = client.post(
#             "/auth/login", json={"email": creds["email"], "password": creds["password"]}
#         )
#         response.raise_for_status()
#         return response.json()["token"]
#
#
# @pytest.fixture
# def authenticated_session(api_client, session_token):
#     api_client.headers["Authorization"] = f"Bearer {session_token}"
#     return api_client
