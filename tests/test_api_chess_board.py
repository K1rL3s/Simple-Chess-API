import os
from pathlib import Path

from dotenv import load_dotenv
import requests

from src.consts import RequestsParams

IMAGES = Path(__file__).absolute().parent / 'board_images'
BASE_URL = "http://127.0.0.1:5000/api/chess/board/"

load_dotenv()

headers = {"Authorization": os.environ.get("API_AUTH_KEY")}


def test_board_fen():
    params = {"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    with open(IMAGES / 'test_board_fen.png', 'rb') as f:
        assert f.read() == response.content


def test_board_size():
    params = {"size": 128, "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "image/png"
    with open(IMAGES / 'test_board_size.png', 'rb') as f:
        assert f.read() == response.content


def test_board_orientation_b():
    for orientation in RequestsParams.BLACK.value:
        params = {"orientation": orientation,  # black
                  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                  "size": 512}
        response = requests.get(BASE_URL, params=params, headers=headers)
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        with open(IMAGES / 'test_board_orientation_b.png', 'rb') as f:
            assert f.read() == response.content


def test_board_orientation_w_or_none():
    for orientation in RequestsParams.WHITE.value:
        params = {"orientation": orientation,
                  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                  "size": 512}
        response = requests.get(BASE_URL, params=params, headers=headers)
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        with open(IMAGES / 'test_board_orientation_w_or_none.png', 'rb') as f:
            assert f.read() == response.content

    params = {"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
              "size": 512}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    with open(IMAGES / 'test_board_orientation_w_or_none.png', 'rb') as f:
        assert f.read() == response.content


def test_board_coords_f():
    for coords in RequestsParams.NO.value:
        params = {"coords": coords,
                  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                  "size": 512}
        response = requests.get(BASE_URL, params=params, headers=headers)
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        with open(IMAGES / 'test_board_coords_f.png', 'rb') as f:
            assert f.read() == response.content


def test_board_coords_t_or_none():
    for coords in RequestsParams.YES.value:
        params = {"coords": coords,
                  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                  "size": 512}
        response = requests.get(BASE_URL, params=params, headers=headers)
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"
        with open(IMAGES / 'test_board_coords_t.png', 'rb') as f:
            assert f.read() == response.content

    params = {"fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
              "size": 512}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    with open(IMAGES / 'test_board_coords_t.png', 'rb') as f:
        assert f.read() == response.content


def test_board_colors():
    params = {"colors": "square light-ffffff;square dark-000000;margin-888888;coord-ff0000",
              "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
              "size": 512}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    with open(IMAGES / 'test_board_colors.png', 'rb') as f:
        assert f.read() == response.content


def test_board_last_move():
    params = {"last_move": "e7e5",  # bad param - ignoring param
              "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
              "size": 512}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    with open(IMAGES / 'test_board_last_move.png', 'rb') as f:
        assert f.read() == response.content


def test_board_check():
    params = {"check": "e8",  # bad param - ignoring param
              "fen": "r1bqkbnr/ppp2Qpp/2np4/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
              "size": 512}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    with open(IMAGES / 'test_board_check.png', 'rb') as f:
        assert f.read() == response.content


def test_board_impossible_fen():
    params = {"fen": "rnb2bnr/pppppppp/8/3Qk3/3qK3/8/PPPPPPPP/RNB2BNR w HAha - 0 1",
              "size": 512}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    with open(IMAGES / 'test_board_impossible_fen.png', 'rb') as f:
        assert f.read() == response.content


def test_board_invalid_fen_or_none():
    params = {"fen": "invalid_fen_string"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data

    params.clear()
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_board_invalid_orientation():
    params = {"orientation": "g"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_board_invalid_coords():
    params = {"coords": "g",  # invalid param
              "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_board_invalid_colors():
    params = {"colors": "invalid_colors",  # it will be an error or ignoring this param
              "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data


def test_board_invalid_size():
    params = {"size": "invalid",
              "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert "message" in data
    assert "status_code" in data
