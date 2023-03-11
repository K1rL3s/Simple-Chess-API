import pytest  # noqa
import requests  # noqa


BASE_URL = "http://127.0.0.1:5000/api/chess/board/"


def test_board_with_fen_and_size():
    params = {"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "size": 512}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"


def test_board_with_size():
    params = {"size": 1024}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"


def test_board_successful():
    params = {"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
              "orientation": "w",
              "size": 1024}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_board_missing_fen_position():
    params = {"orientation": "b", "size": 240}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_board_invalid_parameter_value():
    params = {"fen": "invalid_fen_string", "size": 512}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 400
    assert "message" in response.json()["response"]
