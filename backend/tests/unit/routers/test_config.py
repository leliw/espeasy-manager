import re

from ampf.testing import ApiTestClient


def test_get_client_config(client: ApiTestClient):
    # When: A GET request is made to /api/config
    response = client.get("/api/config")
    r = response.json()
    # Then: The response status code is 200
    assert 200 == response.status_code
    # And: The response has "version"
    assert 1 == len(r)
    pattern = r"^\d+\.\d+\.\d+$"
    assert re.match(pattern, r["version"])
