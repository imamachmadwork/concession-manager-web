import pytest


@pytest.mark.smoke
def test_get_post(api_client):
    response = api_client.get("/posts/1")
    response.raise_for_status()
    assert response.json()["id"] == 1
