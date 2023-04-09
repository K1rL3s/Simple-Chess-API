from random import randint

from src.consts import Limits
from src.utils.limitations import limit_engine_params, limit_board_params


def test_limit_engine_minimum():
    min_time = 0
    threads = 0
    depth = 0
    ram_hash = 0
    skill_level = 0
    elo = 0

    min_time, threads, depth, ram_hash, skill_level, elo = limit_engine_params(min_time, threads, depth, ram_hash,
                                                                               skill_level, elo)
    assert Limits.MIN_THINK_MS.value == min_time
    assert Limits.MIN_THREADS.value == threads
    assert Limits.MIN_DEPTH.value == depth
    assert Limits.MIN_RAM_HASH.value == ram_hash
    assert Limits.MIN_SKILL_LEVEL.value == skill_level
    assert Limits.MIN_ELO.value == elo


def test_limit_engine_maximum():
    min_time = 10 ** 9
    threads = 10 ** 9
    depth = 10 ** 9
    ram_hash = 10 ** 9
    skill_level = 10 ** 9
    elo = 10 ** 9

    min_time, threads, depth, ram_hash, skill_level, elo = limit_engine_params(min_time, threads, depth, ram_hash,
                                                                               skill_level, elo)
    assert Limits.MAX_THINK_MS.value == min_time
    assert Limits.MAX_THREADS.value == threads
    assert Limits.MAX_DEPTH.value == depth
    assert Limits.MAX_RAM_HASH.value == ram_hash
    assert Limits.MAX_SKILL_LEVEL.value == skill_level
    assert Limits.MAX_ELO.value == elo


def test_limit_engine_random():
    min_time = randint(0, 10 ** 9)
    threads = randint(0, 10 ** 9)
    depth = randint(0, 10 ** 9)
    ram_hash = randint(0, 10 ** 9)
    skill_level = randint(0, 10 ** 9)
    elo = randint(0, 10 ** 9)

    min_time, threads, depth, ram_hash, skill_level, elo = limit_engine_params(min_time, threads, depth, ram_hash,
                                                                               skill_level, elo)
    assert Limits.MIN_THINK_MS.value <= min_time <= Limits.MAX_THINK_MS.value
    assert Limits.MIN_THREADS.value <= threads <= Limits.MAX_THREADS.value
    assert Limits.MIN_DEPTH.value <= depth <= Limits.MAX_DEPTH.value
    assert Limits.MIN_RAM_HASH.value <= ram_hash <= Limits.MAX_RAM_HASH.value
    assert Limits.MIN_SKILL_LEVEL.value <= skill_level <= Limits.MAX_SKILL_LEVEL.value
    assert Limits.MIN_ELO.value <= elo <= Limits.MAX_ELO.value


def test_limit_board_minimum():
    size = 0

    size = limit_board_params(size)

    assert Limits.MIN_BOARD_IMAGE_SIZE.value == size


def test_limit_board_maximum():
    size = 10 ** 9

    size = limit_board_params(size)

    assert Limits.MAX_BOARD_IMAGE_SIZE.value == size


def test_limit_board_random():
    size = randint(0, 10 ** 9)

    size = limit_board_params(size)

    assert Limits.MIN_BOARD_IMAGE_SIZE.value <= size <= Limits.MAX_BOARD_IMAGE_SIZE.value
