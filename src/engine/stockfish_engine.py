import os

import stockfish
import chess

from src.consts import engine_params, StatusCodes, Defaults
from src.utils.limitations import limit_engine_params

engine_path = os.environ['STOCKFISH_ENGINE_PATH']


def get_stockfish(
        threads: int = Defaults.THREADS.value,
        depth: int = Defaults.DEPTH.value,
        ram_hash: int = Defaults.RAM_HASH.value,
        skill_level: int = Defaults.SKILL_LEVEL.value,
        elo: int = Defaults.ELO.value,
        previous_moves: str = None
) -> stockfish.Stockfish | None:
    """
    Возвращает instance stockfish.Stockfish с указанными параметрами.

    :param threads: Потоки для работы движка. Больше - сильнее. Должно быть меньше, чем доступно на пк.
    :param depth: Глубина продумывания ходов.
    :param ram_hash: Кол-во оперативный памяти в МБ. Должно быть степенью двойки.
    :param skill_level: Уровень скилла от 1 до 20.
    :param elo: Шахматный рейтинг Эло.
    :param previous_moves: Предыдущие ходы в формате "e2e4;e7e5;...".
    :return: stockfish.Stockfish.
    """

    threads, depth, ram_hash, skill_level, elo = limit_engine_params(threads, depth, ram_hash, skill_level, elo)

    new_params = engine_params.copy()
    new_params.update({
        "Threads": threads,
        "Hash": ram_hash,
        "Skill Level": skill_level,
        "UCI_Elo": elo
    })
    engine = stockfish.Stockfish(
        path=engine_path,
        depth=depth,
        parameters=engine_params
    )

    if previous_moves:
        for move in previous_moves.split(';'):
            answer = make_move(engine, move)
            if answer == StatusCodes.INVALID_PARAMS.value:
                return None

    return engine


def make_move(engine: stockfish.Stockfish, move: str) -> chess.Termination | int | None:
    """
    Делатель хода. Обновляет engine, делая новый ход из текущего положения.

    :param engine: Движок.
    :param move: Ход формата "e2e4".
    :return: Состояние, по которому закончилась игра, или статус-код ошибки.
    """

    if not engine.is_move_correct(move):
        return StatusCodes.INVALID_PARAMS.value
    engine.make_moves_from_current_position([move])
    terminator = is_game_over(engine)
    return terminator.value if terminator is not None else None


def is_game_over(engine: stockfish.Stockfish) -> chess.Termination | None:
    """
    Проверка на конец игры.

    :param engine: Движок.
    :return: Состояние, по которому закончилась игра, или None (не закончилась).
    """

    outcome = chess.Board(engine.get_fen_position()).outcome()
    if outcome is not None:
        return outcome.termination
    return None
