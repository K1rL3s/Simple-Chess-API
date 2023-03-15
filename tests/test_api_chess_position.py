import pytest  # noqa
import requests  # noqa

BASE_URL = "http://127.0.0.1:5000/api/chess/position/"


def test_position_with_fen():
    params = {"fen": "r1bqkbnr/pppppppp/2n5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "is_end" in data
    assert "who_win" in data
    assert "value" in data
    assert 'type' in data
    assert "wdl" in data
    assert "fen" in data


def test_position_with_history():
    params = {"prev_moves": "e2e4;g8f6;f1c4"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "is_end" in data
    assert "who_win" in data
    assert "value" in data
    assert data["value"] is not None
    assert 'type' in data
    assert data["type"] == "cp"
    assert "wdl" in data
    assert data["wdl"] is not None
    assert "fen" in data


def test_position_without_engine():
    params = {"prev_moves": "e2e4;g8f6;f1c4", "with_engine": "f"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "is_end" in data
    assert "who_win" in data
    assert "value" in data
    assert data["value"] is None
    assert 'type' in data
    assert data["type"] is None
    assert "wdl" in data
    assert data["wdl"] is None
    assert "fen" in data


def test_position_checkmate():
    params = {"prev_moves": "e2e4;f7f6;d2d4;g7g5;d1h5"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "is_end" in data
    assert data["is_end"] is True
    assert "who_win" in data
    assert data["who_win"] == 'w'
    assert "value" in data
    assert data["value"] == 0
    assert 'type' in data
    assert data["type"] == "checkmate"
    assert "wdl" in data
    assert data["wdl"] is None
    assert "fen" in data


def test_position_stalemate():
    params = {"fen": "7k/8/6Q1/6K1/8/8/8/8 b - - 0 1"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "is_end" in data
    assert data["is_end"] is True
    assert "who_win" in data
    assert data["who_win"] is None
    assert "value" in data
    assert data["value"] == 0
    assert 'type' in data
    assert data["type"] == "stalemate"
    assert "wdl" in data
    assert data["wdl"] is None
    assert "fen" in data


def test_position_insufficient_material():
    params = {"fen": "7k/8/8/6K1/8/8/8/8 w - - 0 1"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "is_end" in data
    assert data["is_end"] is True
    assert "who_win" in data
    assert data["who_win"] is None
    assert "value" in data
    assert data["value"] == 0
    assert 'type' in data
    assert data["type"] == "insufficient_material"
    assert "wdl" in data
    assert data["wdl"] is not None
    assert "fen" in data


def test_position_evaluation_with_invalid_fen():
    params = {"fen": "invalid_fen"}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 400


def test_position_evaluation_without_params():
    response = requests.get(BASE_URL)
    assert response.status_code == 400


def test_position_evaluation_with_invalid_history():
    params = {"prev_moves": "invalid_moves"}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 400


def test_position_evaluation_with_invalid_params():
    params = {"invalid_param": "invalid_value"}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 400


def test_position_evaluation_with_invalid_engine():
    params = {"with_engine": "g"}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 400
