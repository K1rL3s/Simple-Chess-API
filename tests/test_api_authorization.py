import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:5000/api/chess/"
API_AUTH_KEY = os.getenv("API_AUTH_KEY")


def test_authorization():
    # Запрос без ключа, когда он есть на сервере - 403
    wait_status_code = 403 if API_AUTH_KEY else 200

    params = {"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}
    response = requests.get(BASE_URL + 'board', params=params)

    assert response.status_code == wait_status_code
