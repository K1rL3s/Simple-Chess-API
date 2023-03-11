import pytest  # noqa
import requests  # noqa


BASE_URL = "http://127.0.0.1:5000/api/chess/docs/"


def test_docs_succesful():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
