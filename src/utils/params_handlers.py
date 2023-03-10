import flask

from src.consts import Defaults, StatusCodes
from src.api.json_response import make_json_response
from src.utils.limitations import limit_move_params


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

    threads, depth, ram_hash, skill_level, elo = limit_move_params(threads, depth, ram_hash, skill_level, elo)

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

