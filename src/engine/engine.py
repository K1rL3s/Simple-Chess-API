import os
from io import BytesIO

import stockfish
import chess
from chess.svg import board as board_to_sgv
from cairosvg import svg2png

from src.consts import engine_params, StatusCodes, Defaults
from src.utils.limitations import limit_engine_params, limit_board_params

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

    engine = stockfish.Stockfish(path=engine_path,
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
            if answer == StatusCodes.INVALID_PARAMS.value:
                return None

    return engine


def get_board_image(
        fen_position: str,
        size: int | None = Defaults.BOARD_IMAGE_SIZE.value,
        orientation: bool | None = True,
        colors: dict[str, str] = None,
        last_move: chess.Move | None = None,
        coords: bool = True,
        check: chess.Square | None = None,
) -> BytesIO | None:
    """
    Возвращает BytesIO объект с загруженным изображением шахматной доски.

    :param fen_position: fen-позиция из stockfish.Stockfish.get_fen_position()
    :param size: Размер стороны квадратной картинки.
    :param orientation: Какие фигуры внизу. True - белые.
    :param colors: Словарь типа "тип клетки": "#цвет"
    :param last_move: Последний ход формата "cNcN", для подсветки на доске.
    :param coords: С координатами ли рисовать доску.
    :param check: Клетка, которую нужно подсветить шахом (красный круг).
    :return: BytesIO PNG.
    """

    """
    Возможные ключи для colors:
    ``square light`` (белые клетки),
    ``square dark`` (черные клетка),
    ``square light lastmove`` (белая клетка последний ход),
    ``square dark lastmove`` (черная клетка последний ход),
    ``margin`` (фон координат),
    ``coord`` (числа и буквы),
    ``arrow green``, ``arrow blue``, ``arrow red``, ``arrow yellow``.

    Значения должны выглядеть как ``ffce9e`` (RGB) или ``15781B80`` (RGBA)
    (в случае с GET запросом - без решётки в начале).
    """

    try:
        board = chess.Board(fen_position)
    except ValueError:
        return None

    if colors is None:
        colors = dict()

    size = limit_board_params(size)

    svg_str = board_to_sgv(
        board=board,
        orientation=orientation,
        size=size,
        colors=colors,
        lastmove=last_move,
        coordinates=coords,
        check=check
    )
    return BytesIO(
        svg2png(
            bytestring=svg_str,
            parent_width=size,
            parent_height=size,
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
