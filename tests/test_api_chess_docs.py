import requests

from tests.base import BASE_URL


BASE_URL += "/docs/"


def test_docs_succesful():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
