import requests

from src.consts import Limits, Defaults
from tests.base import BASE_URL, headers


BASE_URL += "/limits/"


def test_limits():
    response = requests.get(BASE_URL, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert 'message' in data
    assert 'status_code' in data
    data = data["response"]

    params = (
        'min_time', 'max_time', 'threads', 'depth',
        'ram_hash', 'skill_level', 'elo', 'size'
    )
    assert len(data.keys()) == len(params)
    assert all([key in params for key in data.keys()])

    assert data["min_time"]["min"] == Limits.MIN_THINK_MS.value
    assert data["min_time"]["default"] == Defaults.THINK_MS.value
    assert data["min_time"]["max"] == Limits.MAX_THINK_MS.value

    assert data["max_time"]["min"] == Limits.MIN_THINK_MS.value
    assert data["max_time"]["default"] == Defaults.THINK_MS.value
    assert data["max_time"]["max"] == Limits.MAX_THINK_MS.value

    assert data["threads"]["min"] == Limits.MIN_THREADS.value
    assert data["threads"]["default"] == Defaults.THREADS.value
    assert data["threads"]["max"] == Limits.MAX_THREADS.value

    assert data["depth"]["min"] == Limits.MIN_DEPTH.value
    assert data["depth"]["default"] == Defaults.DEPTH.value
    assert data["depth"]["max"] == Limits.MAX_DEPTH.value

    assert data["ram_hash"]["min"] == Limits.MIN_RAM_HASH.value
    assert data["ram_hash"]["default"] == Defaults.RAM_HASH.value
    assert data["ram_hash"]["max"] == Limits.MAX_RAM_HASH.value

    assert data["skill_level"]["min"] == Limits.MIN_SKILL_LEVEL.value
    assert data["skill_level"]["default"] == Defaults.SKILL_LEVEL.value
    assert data["skill_level"]["max"] == Limits.MAX_SKILL_LEVEL.value

    assert data["elo"]["min"] == Limits.MIN_ELO.value
    assert data["elo"]["default"] == Defaults.ELO.value
    assert data["elo"]["max"] == Limits.MAX_ELO.value

    assert data["size"]["min"] == Limits.MIN_BOARD_IMAGE_SIZE.value
    assert data["size"]["default"] == Defaults.BOARD_IMAGE_SIZE.value
    assert data["size"]["max"] == Limits.MAX_BOARD_IMAGE_SIZE.value
