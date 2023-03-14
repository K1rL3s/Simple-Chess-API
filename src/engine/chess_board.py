from io import BytesIO

import chess
from cairosvg import svg2png
from chess.svg import board as board_to_sgv

from src.consts import Defaults
from src.utils.limitations import limit_board_params


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
