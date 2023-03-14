import chess
import flask

from src.consts import Defaults, StatusCodes
from src.api.json_response import make_json_response


def handle_move_params() -> tuple[str, str, str, int, int, int, int, int] | flask.Response:
    try:
        data = flask.request.args
        user_move = data.get('user_move', '').lower()
        prev_moves = data.get('prev_moves', '').lower()
        orientation = str(data.get('orientation', 'w')).lower()
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
                                  'Invalid param "user_move"')

    if orientation not in ('w', 'b'):
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  'Invalid param "orientation". It must be "w" or "b".')

    if len(prev_moves) > 4 and ';' not in prev_moves:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  'Invalid param "prev_moves". Between moves must be ";".')

    return user_move, prev_moves, orientation, threads, depth, ram_hash, skill_level, elo


def handle_board_params() -> tuple[
                                 str | None,
                                 int | None,
                                 str | None,
                                 dict[str, str] | None,
                                 chess.Move | None,
                                 bool,
                                 chess.Square | None
                             ] | flask.Response:
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
                                  '"fen_position" param is invalid.')

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
                                      '"colors" param is invalid. Between square-type and colors must be "-",'
                                      'between pairs must be ";"')
    else:
        colors = None

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
    data = flask.request.args
    try:
        prev_moves = data.get('prev_moves', '').lower()
        fen_position = data.get('fen')
        with_engine = data.get('engine', 't').lower()
    except Exception as e:
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  str(e))

    if not prev_moves and not fen_position:
        return make_json_response(StatusCodes.INVALID_PARAMS.value,
                                  '"prev_moves" or "fen" param is required')

    if with_engine not in ('t', 'f'):
        return make_json_response(StatusCodes.INVALID_PARAMS,
                                  '"with_engine" param is invalid. It must be "t" (true) or "f" (false).')
    with_engine = with_engine == 'f'

    return prev_moves, fen_position, with_engine
