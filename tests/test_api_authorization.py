import requests

from tests.base import API_AUTH_KEY, BASE_URL


BASE_URL += "/board/"


def test_authorization():
    # Запрос без ключа, когда он есть на сервере - 403
    wait_status_code = 403 if API_AUTH_KEY else 200

    params = {
        "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    }
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == wait_status_code
