import os

import requests
from dotenv import load_dotenv

from src.consts import RequestsParams

BASE_URL = "http://127.0.0.1:5000/api/chess/move/"

load_dotenv()

headers = {"Authorization": os.environ.get("API_AUTH_KEY")}


def test_move_with_user_move_and_prev_moves():
    params = {"user_move": "e2e4", "prev_moves": "d2d4;d7d5;b1c3;g8f6"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert response.status_code == 200
    assert "stockfish_move" in data
    assert "prev_moves" in data
    assert "orientation" in data
    assert data["orientation"] == "w"
    assert "fen" in data
    assert "end_type" in data
    assert "check" in data


def test_move_successful():
    params = {"user_move": "e2e4", "orientation": "w"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "stockfish_move" in data
    assert "prev_moves" in data
    assert "orientation" in data
    assert data["orientation"] == 'w'
    assert "fen" in data
    assert "end_type" in data
    assert "check" in data


def test_move_without_user_move():
    params = {"prev_moves": "e2e4;e7e5;g1f3;b8c6"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "stockfish_move" in data
    assert "prev_moves" in data
    assert "orientation" in data
    assert data["orientation"] == 'b'
    assert "fen" in data
    assert "end_type" in data
    assert "check" in data


def test_move_after_mate():
    params = {"prev_moves": "e2e4;f7f6;d2d4;g7g5;d1h5"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "stockfish_move" in data
    assert data["stockfish_move"] is None
    assert "prev_moves" in data
    assert "orientation" in data
    assert data["orientation"] == 'b'
    assert "fen" in data
    assert "end_type" in data
    assert data["end_type"] == "checkmate"
    assert "check" in data


def test_move_min_time():
    params = {"user_move": "e2e4",
              "orientation": "w",
              "min_time": 5000}  # Чтоб заметнее было в тестах
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "stockfish_move" in data
    assert "prev_moves" in data
    assert "orientation" in data
    assert "fen" in data
    assert "end_type" in data
    assert "check" in data


def test_move_max_time():
    params = {"user_move": "e2e4",
              "orientation": "w",
              "min_time": 1,
              "max_time": 100}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "stockfish_move" in data
    assert "prev_moves" in data
    assert "orientation" in data
    assert "fen" in data
    assert "end_type" in data
    assert "check" in data


def test_move_first_move_with_correct_orientation():
    for orientation in RequestsParams.BLACK.value:
        params = {"orientation": orientation,
                  "max_time": 1}
        response = requests.get(BASE_URL, params=params, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data
        assert 'status_code' in data
        data = data["response"]
        assert "stockfish_move" in data
        assert "prev_moves" in data
        assert "orientation" in data
        assert "fen" in data
        assert "end_type" in data
        assert "check" in data


def test_move_white_move_with_correct_orientation():
    for orientation in RequestsParams.WHITE.value:
        params = {"prev_moves": "e2e4;e7e5",
                  "orientation": orientation,
                  "max_time": 1}
        response = requests.get(BASE_URL, params=params, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data
        assert 'status_code' in data
        data = data["response"]
        assert "stockfish_move" in data
        assert "prev_moves" in data
        assert "orientation" in data
        assert "fen" in data
        assert "end_type" in data
        assert "check" in data


def test_move_with_invalid_max_time():
    params = {"user_move": "e2e4",
              "orientation": "w",
              "max_time": "invalid"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_with_invalid_min_time():
    params = {"user_move": "e2e4",
              "orientation": "w",
              "min_time": "invalid"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_first_move_invalid_orientation():
    params = {"orientation": "w"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_invalid_user_move_char():
    params = {"user_move": "p9p7", "prev_moves": "e2e4;e7e5;g1f3;b8c6"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_invalid_prev_moves():
    params = {"prev_moves": "e2e4;e8e5;g1f3;b8c6"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_with_invalid_orientation():
    params = {"user_move": "e2e4", "orientation": "invalid"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_with_invalid_threads():
    params = {"user_move": "e2e4", "threads": "invalid"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_with_invalid_depth():
    params = {"user_move": "e2e4", "depth": "invalid"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_missing_required_parameter():
    response = requests.get(BASE_URL, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_invalid_user_move_number():
    params = {"user_move": "e0e4"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_invalid_ram_hash():
    params = {"user_move": "e2e4", "ram_hash": "invalid"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_invalid_skill_level():
    params = {"user_move": "e2e4", "skill_level": "invalid"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_move_invalid_elo():
    params = {"user_move": "e2e4", "elo": "invalid"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data
