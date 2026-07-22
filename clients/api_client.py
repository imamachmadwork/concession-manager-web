import os

import httpx


class ApiClient(httpx.Client):
    """Thin httpx.Client wrapper for hitting the backend API directly (no
    browser), scoped to a base URL read from API_BASE_URL.

    If the platform is multi-tenant (each org/customer served from its own
    host), add a resolver here, e.g.:

        def resolve_org_api_base(self, org_slug: str) -> str:
            response = self.get("/search-organizations", params={"q": org_slug})
            response.raise_for_status()
            return response.json()["results"][0]["apiBaseUrl"]

    and call it once per org (see credentials.py) instead of hardcoding a
    single base URL.
    """

    def __init__(self, **kwargs):
        base_url = os.environ.get("API_BASE_URL") or "https://jsonplaceholder.typicode.com"
        super().__init__(base_url=base_url, timeout=15.0, **kwargs)
