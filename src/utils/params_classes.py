from typing import NamedTuple

from chess import Move


class MoveParams(NamedTuple):
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


class BoardParams(NamedTuple):
    fen: str
    size: int
    orientation: bool
    colors: dict | None
    last_move: Move | None
    coords: bool
    check: int | None


class PositionParams(NamedTuple):
    prev_moves: str | None
    fen: str | None
    with_engine: bool
