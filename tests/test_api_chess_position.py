import os

import requests
from dotenv import load_dotenv

from src.consts import RequestsParams


BASE_URL = "http://127.0.0.1:5000/api/chess/position/"

load_dotenv()

headers = {"Authorization": os.environ.get("API_AUTH_KEY")}
PREPARED_ENGINES = int(os.getenv("PREPARED_ENGINES") or 0)


def test_position_with_fen():
    params = {
        "fen": "r1bqkbnr/pppppppp/2n5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "is_end" in data
    assert "who_win" in data
    assert "value" in data
    assert 'end_type' in data
    assert "wdl" in data
    assert "fen" in data


def test_position_with_history():
    params = {
        "prev_moves": "e2e4;g8f6;f1c4"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "is_end" in data
    assert "who_win" in data
    assert "value" in data
    assert data["value"] is not None
    assert 'end_type' in data
    assert data["end_type"] == "cp"
    assert "wdl" in data
    assert data["wdl"] is not None
    assert "fen" in data


def test_position_without_engine():
    params = {
        "prev_moves": "e2e4;g8f6;f1c4",
        "with_engine": "f"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "is_end" in data
    assert "who_win" in data
    assert "value" in data
    assert data["value"] is None
    assert 'end_type' in data
    assert data["end_type"] is None
    assert "wdl" in data
    assert data["wdl"] is None
    assert "fen" in data


def test_position_yes_or_no_engine_param():
    for yes_or_no in RequestsParams.YES_OR_NO.value:
        params = {
            "prev_moves": "e2e4;g8f6;f1c4",
            "with_engine": yes_or_no
        }
        response = requests.get(BASE_URL, params=params, headers=headers)
        assert response.status_code == 200


def test_position_white_win_by_checkmate():
    params = {
        "prev_moves": "e2e4;f7f6;d2d4;g7g5;d1h5"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "is_end" in data
    assert data["is_end"] is True
    assert "who_win" in data
    assert data["who_win"] == 'w'
    assert "value" in data
    assert data["value"] == 0
    assert 'end_type' in data
    assert data["end_type"] == "checkmate"
    assert "wdl" in data
    assert data["wdl"] is None
    assert "fen" in data


def test_position_black_win_by_checkmate():
    fen = "r1b1kbnr/pp2p2p/B1n3p1/2pp3K/4pq2/8/PPPP1PPP/RNBQ2NR w kq - 0 9"
    params = {
        "fen": fen
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "is_end" in data
    assert data["is_end"] is True
    assert "who_win" in data
    assert data["who_win"] == 'b'
    assert "value" in data
    assert data["value"] == 0
    assert 'end_type' in data
    assert data["end_type"] == "checkmate"
    assert "wdl" in data
    assert data["wdl"] is None
    assert "fen" in data


def test_position_stalemate():
    params = {
        "fen": "7k/8/6Q1/6K1/8/8/8/8 b - - 0 1"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "is_end" in data
    assert data["is_end"] is True
    assert "who_win" in data
    assert data["who_win"] is None
    assert "value" in data
    assert data["value"] == 0
    assert 'end_type' in data
    assert data["end_type"] == "stalemate"
    assert "wdl" in data
    assert data["wdl"] is None
    assert "fen" in data


def test_position_insufficient_material():
    params = {
        "fen": "7k/8/8/6K1/8/8/8/8 w - - 0 1"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "is_end" in data
    assert data["is_end"] is True
    assert "who_win" in data
    assert data["who_win"] is None
    assert "value" in data
    assert data["value"] == 0
    assert 'end_type' in data
    assert data["end_type"] == "insufficient_material"
    assert "wdl" in data
    assert data["wdl"] is not None
    assert "fen" in data


def test_position_impossible_fen():
    """
    Даже если передать что-то типа 8/p7/3Kk3/3Kk3/3Kk3/8/7P/8 w - - 0 1,
    то движок будет это оценивать :(
    В библиотеках нет никакой проверки на это, а мне лень.
    (движок вылетает, если попросить сделать ход из такой позиции,
    но ошибку не выдаёт)
    """
    pass


def test_position_fen_prepared_engine():
    fen = "r1b1kbnr/pp2p2p/B1n3p1/2pp3K/4pq2/8/PPPP1PPP/RNBQ2NR w kq - 0 9"
    params = {
        "fen": fen,
        "prepared": "1"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    data = response.json()

    # Если не установлены движки, то должна быть ошибка
    if not PREPARED_ENGINES:
        assert response.status_code == 409
        assert "message" in data
        assert "status_code" in data
        return

    assert response.status_code == 200
    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "is_end" in data
    assert data["is_end"] is True
    assert "who_win" in data
    assert data["who_win"] == 'b'
    assert "value" in data
    assert data["value"] == 0
    assert 'end_type' in data
    assert data["end_type"] == "checkmate"
    assert "wdl" in data
    assert data["wdl"] is None
    assert "fen" in data


def test_position_prev_moves_prepared_engine():
    params = {
        "prev_moves": "e2e4;f7f6;d2d4;g7g5;d1h5",
        "prepared": "1"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    data = response.json()

    if not PREPARED_ENGINES:  # Если не установлены движки, то должна быть ошибка
        assert response.status_code == 409
        assert "message" in data
        assert "status_code" in data
        return

    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]
    assert "is_end" in data
    assert data["is_end"] is True
    assert "who_win" in data
    assert data["who_win"] == 'w'
    assert "value" in data
    assert data["value"] == 0
    assert 'end_type' in data
    assert data["end_type"] == "checkmate"
    assert "wdl" in data
    assert data["wdl"] is None
    assert "fen" in data


def test_position_with_invalid_fen():
    params = {
        "fen": "invalid_fen"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_position_without_params():
    response = requests.get(BASE_URL, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_position_with_invalid_history():
    params = {
        "prev_moves": "invalid_moves"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_position_with_invalid_engine():
    params = {
        "fen": "r1bqkbnr/pppppppp/2n5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1",
        "with_engine": "g"
    }
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data
