from io import BytesIO

import stockfish
import chess
from chess.svg import board as board_to_sgv
from cairosvg import svg2png

from src.consts import STOCKFISH_ENGINE_PATH, engine_params, StatusCodes, Defaults


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

    engine = stockfish.Stockfish(path=STOCKFISH_ENGINE_PATH,
                                 depth=depth,
                                 parameters=engine_params)
    engine.update_engine_parameters(
        {
            "Threads": threads,
            "Hash": ram_hash,
            "Skill Level": skill_level,
            "UCI_Elo": elo
        }
    )

    if previous_moves:
        for move in previous_moves.split(';'):
            answer = make_move(engine, move)
            if answer == StatusCodes.CONFLICT.value:
                return None

    return engine


def get_board_image(
        fen_position: str,
        size: int = Defaults.BOARD_IMAGE_SIZE.value,
        orientation: str = 'w'
) -> BytesIO | None:
    """
    Возвращает BytesIO объект с загруженным изображением шахматной доски.

    :param fen_position: fen-позиция из stockfish.Stockfish.get_fen_position()
    :param size: Размер стороны квадратной картинки.
    :param orientation: Какие фигуры внизу. 'w' или 'b'.
    :return: BytesIO PNG.
    """

    try:
        board = chess.Board(fen_position)
    except ValueError:
        return None

    svg_str = board_to_sgv(
        board,
        orientation=chess.WHITE if orientation == 'w' else chess.BLACK,
        size=size
    )
    return BytesIO(
        svg2png(
            bytestring=svg_str,
            parent_width=size,
            parent_height=size
        )
    )


def make_move(engine: stockfish.Stockfish, move: str) -> chess.Termination | int:
    """
    Делатель хода. Обновляет engine, делая новый ход из текущего положения.
    :param engine: Движок.
    :param move: Ход формата "e2e4".
    :return: Состояние, по которому закончилась игра, или статус-код ошибки.
    """

    if not engine.is_move_correct(move):
        return StatusCodes.CONFLICT.value
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
