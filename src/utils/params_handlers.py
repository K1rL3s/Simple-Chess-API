import chess
import flask

from src.consts import Defaults, StatusCodes, Limits, RequestsParams
from src.utils.params_classes import BoardParams, MoveParams, PositionParams
from src.utils.abort import abort


def handle_move_params() -> MoveParams:
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
        prepared = data.get('prepared', 'f').lower()
    except Exception as e:
        return abort(StatusCodes.INVALID_PARAMS, str(e))

    # Обработка некорректных данных
    if not user_move and not prev_moves and orientation not in RequestsParams.BLACK.value:
        # Если не задан ход, раньше ходов не было и игрок не играет за чёрных
        # Нужно, чтобы машина играла белыми (сделала первый ход)
        abort(StatusCodes.INVALID_PARAMS, '"user_move" param is invalid')

    if min_time > max_time:
        max_time = min_time

    if orientation not in RequestsParams.COLORS.value:
        abort(
            StatusCodes.INVALID_PARAMS,
            f'"orientation" param is invalid. It must be in {RequestsParams.COLORS.value}'
        )
    orientation = 'w' if orientation in RequestsParams.WHITE.value else 'b'

    if len(prev_moves) > 4 and ';' not in prev_moves:
        abort(
            StatusCodes.INVALID_PARAMS,
            '"prev_moves" param is invalid. Between moves must be ";".'
        )

    if prepared not in RequestsParams.YES_OR_NO.value:
        abort(
            StatusCodes.INVALID_PARAMS,
            f'"prepared" param is invalid. It must in {RequestsParams.YES_OR_NO.value}'
        )
    prepared = prepared in RequestsParams.YES.value

    return MoveParams(
        user_move=user_move,
        prev_moves=prev_moves,
        orientation=orientation,
        min_time=min_time,
        max_time=max_time,
        threads=threads,
        depth=depth,
        ram_hash=ram_hash,
        skill_level=skill_level,
        elo=elo,
        prepared=prepared,
    )


def handle_board_params() -> BoardParams:
    """
    Обработчик параметров на запрос рисования доски.
    """

    data = flask.request.args
    try:
        fen = data.get('fen', '')
        size = int(data.get('size', Defaults.BOARD_IMAGE_SIZE.value))
        orientation = data.get('orientation', 'w').lower()
        colors = data.get('colors', '').lower()
        last_move = data.get('last_move', '').upper()
        coords = data.get('coords', 't').lower()
        check = data.get('check', '').upper()
    except Exception as e:
        return abort(StatusCodes.INVALID_PARAMS, str(e))

    if not fen:
        abort(StatusCodes.INVALID_PARAMS, '"fen" param is invalid')

    if orientation not in RequestsParams.COLORS.value:
        abort(
            StatusCodes.INVALID_PARAMS,
            f'"orientation" param is invalid. It must be in {RequestsParams.COLORS.value}'
        )
    # orientation = orientation == 'w'
    # Здесь такая обработка, потому что для библиотеки chess
    orientation = chess.WHITE if orientation in RequestsParams.WHITE.value else chess.BLACK

    if colors:
        try:
            colors = {square: f'#{color}' for square, color in
                      [pair.split('-') for pair in colors.split(';')]}
        except ValueError:
            abort(
                StatusCodes.INVALID_PARAMS,
                '"colors" param is invalid. Between square-type and colors must be "-", '
                'between pairs must be ";"'
            )
    else:
        colors = None

    # Узнал про chess.Move.from_uci, но там за неверный код ошибку даёт,
    # поэтому оставлю это чудо ниже. :)
    if (s1 := getattr(chess, last_move[:2].upper(), None)) is not None and \
            (s2 := getattr(chess, last_move[2:].upper(), None)) is not None:
        last_move = chess.Move(s1, s2)
    else:
        last_move = None

    if coords not in RequestsParams.YES_OR_NO.value:
        abort(
            StatusCodes.INVALID_PARAMS,
            f'"coords" param is invalid. It must in {RequestsParams.YES_OR_NO.value}'
        )
    coords = coords in RequestsParams.YES.value

    check = getattr(chess, check, None)

    return BoardParams(
        fen=fen,
        size=size,
        orientation=orientation,
        colors=colors,
        last_move=last_move,
        coords=coords,
        check=check,
    )


def handle_position_params() -> PositionParams:
    """
    Обработчик параметров на оценку позиции.
    """

    data = flask.request.args
    try:
        prev_moves = data.get('prev_moves', '').lower()
        fen = data.get('fen', '')
        with_engine = data.get('with_engine', 't').lower()
        prepared = data.get('prepared', 'f').lower()
    except Exception as e:
        return abort(StatusCodes.INVALID_PARAMS, str(e))

    if not prev_moves and not fen:
        abort(
            StatusCodes.INVALID_PARAMS.value,
            '"prev_moves" or "fen" param is required'
        )

    if fen:
        try:
            chess.Board(fen)
        except ValueError:
            abort(
                StatusCodes.INVALID_PARAMS,
                '"fen" param is invalid'
            )

    if with_engine not in RequestsParams.YES_OR_NO.value:
        abort(
            StatusCodes.INVALID_PARAMS,
            f'"with_engine" param is invalid. It must in {RequestsParams.YES_OR_NO.value}'
        )
    with_engine = with_engine in RequestsParams.YES.value

    if prepared not in RequestsParams.YES_OR_NO.value:
        abort(
            StatusCodes.INVALID_PARAMS,
            f'"prepared" param is invalid. It must in {RequestsParams.YES_OR_NO.value}'
        )
    prepared = prepared in RequestsParams.YES.value

    return PositionParams(
        prev_moves=prev_moves,
        fen=fen,
        with_engine=with_engine,
        prepared=prepared,
    )
