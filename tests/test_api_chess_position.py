import pytest  # noqa
import requests  # noqa

BASE_URL = "http://127.0.0.1:5000/api/chess/position/"


def test_position_evaluation_without_history():
    params = {"fen": "r1bqkbnr/pppppppp/2n5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "is_end" in data
    assert "who_win" in data
    assert "value" in data
    assert "wdl" in data
    assert "fen" in data


def test_position_evaluation_with_history():
    params = {"prev_moves": "e2e4;g8f6;f1c4"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()["response"]
    assert response.status_code == 200
    assert "is_end" in data
    assert "who_win" in data
    assert "value" in data
    assert "wdl" in data
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
