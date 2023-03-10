import pytest  # noqa
import requests  # noqa


BASE_URL = "http://127.0.0.1:5000/api/chess"


def test_move_with_user_move_and_prev_moves():
    params = {"user_move": "e2e4", "prev_moves": "d2d4;d7d5;b1c3;g8f6"}
    response = requests.get(BASE_URL + "/move/", params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "stockfish_move" in data
    assert "prev_moves" in data
    assert "orientation" in data
    assert "fen" in data


def test_move_with_orientation():
    params = {"orientation": "b"}
    response = requests.get(BASE_URL + "/move/", params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "stockfish_move" in data
    assert "prev_moves" in data
    assert "orientation" in data
    assert "fen" in data
    assert data["orientation"] == "b"


def test_move_successful():
    params = {"user_move": "e2e4", "orientation": "w"}
    response = requests.get(BASE_URL + "/move/", params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "stockfish_move" in data
    assert "prev_moves" in data
    assert "orientation" in data
    assert "fen" in data


def test_move_without_user_move():
    params = {"orientation": "w"}
    response = requests.get(BASE_URL + "/move/", params=params)
    assert response.status_code == 400


def test_move_invalid_user_move_char():
    params = {"user_move": "p9p7", "prev_moves": "e2e4;e7e5;g1f3;b8c6"}
    response = requests.get(BASE_URL + "/move/", params=params)
    assert response.status_code == 409


def test_move_with_invalid_orientation():
    params = {"user_move": "e2e4", "orientation": "invalid"}
    response = requests.get(BASE_URL + "/move/", params=params)
    assert response.status_code == 400


def test_move_with_invalid_threads():
    params = {"user_move": "e2e4", "threads": "invalid"}
    response = requests.get(BASE_URL + "/move/", params=params)
    assert response.status_code == 400


def test_move_with_invalid_depth():
    params = {"user_move": "e2e4", "depth": "invalid"}
    response = requests.get(BASE_URL + "/move/", params=params)
    assert response.status_code == 400


def test_move_missing_required_parameter():
    response = requests.get(BASE_URL + "/move/")
    assert response.status_code == 400
    assert "message" in response.json()["response"]


def test_move_invalid_user_move_number():
    params = {"user_move": "e0e4"}
    response = requests.get(BASE_URL + "/move/", params=params)
    assert response.status_code == 409
    assert "message" in response.json()["response"]
