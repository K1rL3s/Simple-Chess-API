import chess
import flask

from src.consts import Defaults, StatusCodes, Limits
from src.api.json_response import make_json_response


def handle_move_params() -> tuple[str, str, str, int, int, int, int, int, int, int] | flask.Response:
    """
    Обработчик параметров на запрос делания хода.
    """

    try:
        data = flask.request.args
        user_move = data.get('user_move', '').lower()
        prev_moves = data.get('prev_moves', '').lower()
        orientation = str(data.get('orientation', 'w')).lower()
        min_time = int(data.get('min_time', Limits.MIN_THINK_MS.value))
        max_time = int(data.get('max_time', Defaults.THINK_MS.value))
        threads = int(data.get('threads', Defaults.THREADS.value))
        depth = int(data.get('depth', Defaults.DEPTH.value))
        ram_hash = int(data.get('ram_hash', Defaults.RAM_HASH.value))
        skill_level = int(data.get('skill_level', Defaults.SKILL_LEVEL.value))
        elo = int(data.get('elo', Defaults.ELO.value))
    except Exception as e:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  str(e))

    # Обработка некорректных данных
    if not user_move and not prev_moves and orientation != 'b':
        # Если не задан ход, раньше ходов не было и игрок не играет за чёрных
        # Нужно, чтобы машина играла белыми (сделала первый ход)
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"user_move" param is invalid')

    if min_time > max_time:
        max_time = min_time

    if orientation not in ('w', 'b'):
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"orientation" param is invalid. It must be "w" or "b".')

    if len(prev_moves) > 4 and ';' not in prev_moves:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"prev_moves" param is invalid. Between moves must be ";".')

    return user_move, prev_moves, orientation, min_time, max_time, threads, depth, ram_hash, skill_level, elo


def handle_board_params() -> tuple[
                                 str | None,
                                 int | None,
                                 str | None,
                                 dict[str, str] | None,
                                 chess.Move | None,
                                 bool,
                                 chess.Square | None
                             ] | flask.Response:
    """
    Обработчик параметров на запрос рисования доски.
    """

    data = flask.request.args
    try:
        fen_position = data.get('fen')
        size = int(data.get('size', Defaults.BOARD_IMAGE_SIZE.value))
        orientation = data.get('orientation', 'w').lower()
        colors = data.get('colors', '').lower()
        last_move = data.get('last_move', '').upper()
        coords = data.get('coords', 't').lower()
        check = data.get('check', '').upper()
    except Exception as e:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  str(e))

    if not fen_position:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"fen_position" param is invalid')

    if orientation not in ('w', 'b'):
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"orientation" param is invalid. It must be "w" or "b".')
    orientation = chess.WHITE if orientation == 'w' else chess.BLACK  # orientation = orientation == 'w'

    if colors:
        try:
            colors = {square: f'#{color}' for square, color in
                      [pair.split('-') for pair in colors.split(';')]}
        except ValueError:
            return make_json_response(StatusCodes.INVALID_PARAMS,
                                      '"colors" param is invalid. Between square-type and colors must be "-", '
                                      'between pairs must be ";"')
    else:
        colors = None

    # Узнал про chess.Move.from_uci, но там за неверный код ошибку даёт, поэтому оставлю это чудо ниже. :)
    if (s1 := getattr(chess, last_move[:2].upper(), None)) is not None and \
            (s2 := getattr(chess, last_move[2:].upper(), None)) is not None:
        last_move = chess.Move(s1, s2)
    else:
        last_move = None

    if coords not in ('t', 'f'):
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"coords" param is invalid. It must be "t" (true) or "f" (false).')
    coords = True if coords == 't' else False

    check = getattr(chess, check, None)

    return fen_position, size, orientation, colors, last_move, coords, check


def handle_position_params() -> tuple[str | None, str | None, bool] | flask.Response:
    """
    Обработчик параметров на оценку позиции.
    """

    data = flask.request.args
    try:
        prev_moves = data.get('prev_moves', '').lower()
        fen_position = data.get('fen')
        with_engine = data.get('with_engine', 't').lower()
    except Exception as e:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  str(e))

    if not prev_moves and not fen_position:
        return make_json_response(StatusCodes.INVALID_PARAMS.value,
                                  '"prev_moves" or "fen" param is required')

    if with_engine not in ('t', 'f'):
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"with_engine" param is invalid. It must be "t" (true) or "f" (false).')
    with_engine = with_engine == 't'

    return prev_moves, fen_position, with_engine
