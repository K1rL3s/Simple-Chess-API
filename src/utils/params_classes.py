from typing import NamedTuple

from chess import Move


class MoveParams(NamedTuple):
    """
    Параметры для роута с "генерацией" ходов.
    """
    user_move: str
    prev_moves: str
    orientation: str
    min_time: int
    max_time: int
    threads: int
    depth: int
    ram_hash: int
    skill_level: int
    elo: int
    prepared: bool


class BoardParams(NamedTuple):
    """
    Параметры для роута с изображением доски.
    """
    fen: str
    size: int
    orientation: bool
    colors: dict | None
    last_move: Move | None
    coords: bool
    check: int | None


class PositionParams(NamedTuple):
    """
    Параметры для роута с оценкой позиции.
    """
    prev_moves: str | None
    fen: str | None
    with_engine: bool
    prepared: bool
